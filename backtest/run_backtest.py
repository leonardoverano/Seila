"""CLI: baixa dados Dukascopy, roda as 30 estratégias e gera relatório comparativo.

Uso:
    python3 -m backtest.run_backtest EURUSD 2024-01-01 2024-03-31 --payout 0.85 --stake 1
"""

from __future__ import annotations

import argparse
import datetime as dt

import pandas as pd

from . import strategies as strat_module
from .dukascopy_downloader import download_ticks, ticks_to_ohlc
from .engine import breakeven_win_rate, run_backtest


def build_dataset(symbol: str, start: dt.date, end: dt.date, timeframes: list[str]) -> dict[str, pd.DataFrame]:
    ticks = download_ticks(symbol, start, end)
    print(f"[dados] {len(ticks)} ticks baixados para {symbol} de {start} a {end}")
    out = {}
    for tf in timeframes:
        ohlc = ticks_to_ohlc(ticks, tf)
        out[tf] = ohlc
        print(f"[dados] {tf}: {len(ohlc)} candles")
    return out


def main():
    parser = argparse.ArgumentParser(description="Backtest das 30 estratégias de opções binárias")
    parser.add_argument("symbol", help="Ex.: EURUSD")
    parser.add_argument("start", help="YYYY-MM-DD")
    parser.add_argument("end", help="YYYY-MM-DD")
    parser.add_argument("--payout", type=float, default=0.85)
    parser.add_argument("--stake", type=float, default=1.0)
    parser.add_argument("--balance", type=float, default=100.0)
    parser.add_argument("--out", default="backtest_report.csv")
    args = parser.parse_args()

    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)

    datasets = build_dataset(args.symbol, start, end, ["1min", "5min", "15min"])

    results = []
    for name, (fn, timeframe, expiration) in strat_module.STRATEGIES.items():
        df = datasets[timeframe].dropna()
        if len(df) < 120:
            print(f"[aviso] {name}: dados insuficientes em {timeframe}, pulando")
            continue
        try:
            signals = fn(df)
        except Exception as exc:  # noqa: BLE001
            print(f"[erro] {name}: {exc}")
            continue
        res = run_backtest(
            df.close, signals, expiration, payout=args.payout, stake=args.stake,
            initial_balance=args.balance, strategy_name=name,
        )
        results.append(res.summary_row())
        print(f"[{name}] trades={res.trades} win_rate={res.win_rate*100:.1f}% roi={res.roi_pct:.1f}%")

    # Estratégia 29 (confluência multi-timeframe) tratada à parte, precisa dos 3 timeframes
    df_m1, df_m5, df_m15 = datasets["1min"].dropna(), datasets["5min"].dropna(), datasets["15min"].dropna()
    if len(df_m1) > 200 and len(df_m5) > 60 and len(df_m15) > 30:
        sig29 = strat_module.s29_mtf_confluence(df_m1, df_m5, df_m15)
        res29 = run_backtest(df_m1.close, sig29, 3, payout=args.payout, stake=args.stake,
                              initial_balance=args.balance, strategy_name="29_mtf_confluence")
        results.append(res29.summary_row())
        print(f"[29_mtf_confluence] trades={res29.trades} win_rate={res29.win_rate*100:.1f}% roi={res29.roi_pct:.1f}%")

    report = pd.DataFrame(results).sort_values("roi_pct", ascending=False)
    report.to_csv(args.out, index=False)
    print(f"\nBreak-even de acerto para payout {args.payout*100:.0f}%: {breakeven_win_rate(args.payout)*100:.2f}%")
    print(f"Relatório salvo em {args.out}")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
