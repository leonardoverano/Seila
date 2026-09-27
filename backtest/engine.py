"""Motor de backtest de opções binárias.

Uma opção binária não é "comprar/vender o ativo": é uma aposta de payoff fixo.
- Sinal CALL na vela i, expiração de N velas: se close[i+N] > close[i] -> vitória (paga `payout`%).
- Sinal PUT: vitória se close[i+N] < close[i].
- Empate (close[i+N] == close[i]): tratado como devolução do valor investido (comum em várias corretoras).
- Derrota: perde 100% do valor investido na operação.

`signals` é uma pd.Series alinhada ao índice do OHLC, com valores em {"CALL", "PUT", None/NaN}.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    strategy: str
    trades: int
    wins: int
    losses: int
    ties: int
    win_rate: float
    payout: float
    stake: float
    roi_pct: float
    final_balance: float
    max_drawdown_pct: float
    equity_curve: pd.Series = field(repr=False)

    def summary_row(self) -> dict:
        return {
            "strategy": self.strategy,
            "trades": self.trades,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "win_rate_pct": round(self.win_rate * 100, 2),
            "roi_pct": round(self.roi_pct, 2),
            "final_balance": round(self.final_balance, 2),
            "max_drawdown_pct": round(self.max_drawdown_pct, 2),
        }


def run_backtest(
    close: pd.Series,
    signals: pd.Series,
    expiration_bars: int,
    payout: float = 0.85,
    stake: float = 1.0,
    initial_balance: float = 100.0,
    strategy_name: str = "",
) -> BacktestResult:
    close = close.reset_index(drop=True)
    signals = signals.reset_index(drop=True)

    n = len(close)
    balance = initial_balance
    equity = [balance]
    wins = losses = ties = 0

    idx = np.where(signals.notna())[0]
    for i in idx:
        j = i + expiration_bars
        if j >= n:
            continue
        entry_price = close.iloc[i]
        exit_price = close.iloc[j]
        direction = signals.iloc[i]

        if exit_price == entry_price:
            ties += 1
            # devolução: saldo não muda
        elif (direction == "CALL" and exit_price > entry_price) or (
            direction == "PUT" and exit_price < entry_price
        ):
            wins += 1
            balance += stake * payout
        else:
            losses += 1
            balance -= stake

        equity.append(balance)

    trades = wins + losses + ties
    equity_series = pd.Series(equity)
    running_max = equity_series.cummax()
    drawdown = (equity_series - running_max) / running_max.replace(0, np.nan)
    max_dd = float(drawdown.min() * 100) if trades > 0 else 0.0

    win_rate = wins / trades if trades else 0.0
    roi_pct = (balance - initial_balance) / initial_balance * 100

    return BacktestResult(
        strategy=strategy_name,
        trades=trades,
        wins=wins,
        losses=losses,
        ties=ties,
        win_rate=win_rate,
        payout=payout,
        stake=stake,
        roi_pct=roi_pct,
        final_balance=balance,
        max_drawdown_pct=max_dd,
        equity_curve=equity_series,
    )


def breakeven_win_rate(payout: float) -> float:
    """Taxa de acerto mínima para ROI = 0 dado o payout (ex.: 0.85 -> ~54.05%)."""
    return 1 / (1 + payout)
