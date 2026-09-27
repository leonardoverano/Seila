"""Indicadores técnicos implementados em pandas/numpy puro (sem TA-Lib)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def bollinger_bands(close: pd.Series, period: int = 20, std_mult: float = 2.0):
    mid = sma(close, period)
    std = close.rolling(period).std(ddof=0)
    upper = mid + std_mult * std
    lower = mid - std_mult * std
    return upper, mid, lower


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    return out.fillna(50)


def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, k_period=5, d_period=3, smooth=3):
    lowest = low.rolling(k_period).min()
    highest = high.rolling(k_period).max()
    raw_k = 100 * (close - lowest) / (highest - lowest).replace(0, np.nan)
    k = raw_k.rolling(smooth).mean()
    d = k.rolling(d_period).mean()
    return k, d


def macd(close: pd.Series, fast=12, slow=26, signal=9):
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def cci(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 20) -> pd.Series:
    tp = (high + low + close) / 3
    sma_tp = sma(tp, period)
    mean_dev = tp.rolling(period).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    return (tp - sma_tp) / (0.015 * mean_dev.replace(0, np.nan))


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr_atr = atr(high, low, close, period)
    plus_di = 100 * pd.Series(plus_dm, index=high.index).ewm(alpha=1 / period, adjust=False).mean() / tr_atr
    minus_di = 100 * pd.Series(minus_dm, index=high.index).ewm(alpha=1 / period, adjust=False).mean() / tr_atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / period, adjust=False).mean()


def parabolic_sar(high: pd.Series, low: pd.Series, step=0.02, max_step=0.2) -> pd.Series:
    length = len(high)
    sar = np.zeros(length)
    trend_up = True
    af = step
    ep = high.iloc[0]
    sar[0] = low.iloc[0]
    for i in range(1, length):
        prev_sar = sar[i - 1]
        if trend_up:
            sar[i] = prev_sar + af * (ep - prev_sar)
            sar[i] = min(sar[i], low.iloc[i - 1], low.iloc[i - 2] if i > 1 else low.iloc[i - 1])
            if high.iloc[i] > ep:
                ep = high.iloc[i]
                af = min(af + step, max_step)
            if low.iloc[i] < sar[i]:
                trend_up = False
                sar[i] = ep
                ep = low.iloc[i]
                af = step
        else:
            sar[i] = prev_sar + af * (ep - prev_sar)
            sar[i] = max(sar[i], high.iloc[i - 1], high.iloc[i - 2] if i > 1 else high.iloc[i - 1])
            if low.iloc[i] < ep:
                ep = low.iloc[i]
                af = min(af + step, max_step)
            if high.iloc[i] > sar[i]:
                trend_up = True
                sar[i] = ep
                ep = high.iloc[i]
                af = step
    return pd.Series(sar, index=high.index)


def donchian_channel(high: pd.Series, low: pd.Series, period: int = 10):
    upper = high.rolling(period).max()
    lower = low.rolling(period).min()
    return upper, lower


def keltner_channel(high: pd.Series, low: pd.Series, close: pd.Series, period=20, atr_mult=2.0):
    mid = ema(close, period)
    band = atr(high, low, close, period) * atr_mult
    return mid + band, mid, mid - band


def vwap_rolling(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 20) -> pd.Series:
    tp = (high + low + close) / 3
    pv = tp * volume
    return pv.rolling(window).sum() / volume.rolling(window).sum().replace(0, np.nan)


def linreg_channel(close: pd.Series, period: int = 20, mult: float = 2.0):
    def _slope_intercept(y):
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        return slope * (len(y) - 1) + intercept

    mid = close.rolling(period).apply(_slope_intercept, raw=True)
    resid_std = close.rolling(period).std(ddof=0)
    upper = mid + mult * resid_std
    lower = mid - mult * resid_std
    return upper, mid, lower


def ichimoku(high: pd.Series, low: pd.Series, tenkan=9, kijun=26, senkou_b=52):
    tenkan_sen = (high.rolling(tenkan).max() + low.rolling(tenkan).min()) / 2
    kijun_sen = (high.rolling(kijun).max() + low.rolling(kijun).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun)
    senkou_span_b = ((high.rolling(senkou_b).max() + low.rolling(senkou_b).min()) / 2).shift(kijun)
    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b


def swing_highs_lows(high: pd.Series, low: pd.Series, order: int = 3):
    """Detecta topos/fundos locais (pivots) usando janela simétrica de `order` candles."""
    highs = pd.Series(False, index=high.index)
    lows = pd.Series(False, index=low.index)
    for i in range(order, len(high) - order):
        window_h = high.iloc[i - order : i + order + 1]
        window_l = low.iloc[i - order : i + order + 1]
        if high.iloc[i] == window_h.max() and (window_h == high.iloc[i]).sum() == 1:
            highs.iloc[i] = True
        if low.iloc[i] == window_l.min() and (window_l == low.iloc[i]).sum() == 1:
            lows.iloc[i] = True
    return highs, lows
