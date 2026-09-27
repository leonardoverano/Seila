"""Implementação das 30 estratégias do guia de scalping como geradores de sinal.

Cada função recebe um DataFrame OHLC (colunas: open, high, low, close) e
retorna uma pd.Series alinhada ao índice com valores em {"CALL", "PUT", NaN}.

Convenção: o sinal na vela i é decidido com dados até o fechamento da vela i
(nada de look-ahead) e a operação "entra" no fechamento dessa mesma vela,
expirando `expiration_bars` velas à frente (ver engine.py).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import indicators as ind


def _empty(df: pd.DataFrame) -> pd.Series:
    return pd.Series(np.nan, index=df.index, dtype=object)


# ---------------------------------------------------------------------------
# Grupo 1 — 10s a 1min (índices 1-20)
# ---------------------------------------------------------------------------

def s01_bollinger_reversal(df):
    upper, mid, lower = ind.bollinger_bands(df.close, 20, 2.0)
    sig = _empty(df)
    touched_lower = df.low.shift(1) <= lower.shift(1)
    touched_upper = df.high.shift(1) >= upper.shift(1)
    back_inside_up = df.close > lower
    back_inside_dn = df.close < upper
    band_width = (upper - lower) / mid
    stable = band_width < band_width.rolling(20).mean() * 1.3
    sig[touched_lower & back_inside_up & stable] = "CALL"
    sig[touched_upper & back_inside_dn & stable] = "PUT"
    return sig


def s02_ema_cross_fast(df):
    ema3, ema8, ema21 = ind.ema(df.close, 3), ind.ema(df.close, 8), ind.ema(df.close, 21)
    cross_up = (ema3 > ema8) & (ema3.shift(1) <= ema8.shift(1))
    cross_dn = (ema3 < ema8) & (ema3.shift(1) >= ema8.shift(1))
    sig = _empty(df)
    sig[cross_up & (df.close > ema21)] = "CALL"
    sig[cross_dn & (df.close < ema21)] = "PUT"
    return sig


def s03_pinbar_sr(df, lookback=25):
    body = (df.close - df.open).abs()
    rng = df.high - df.low
    upper_wick = df.high - df[["open", "close"]].max(axis=1)
    lower_wick = df[["open", "close"]].min(axis=1) - df.low
    support = df.low.rolling(lookback).min()
    resistance = df.high.rolling(lookback).max()
    pin_bull = (lower_wick > body * 2) & (rng > 0)
    pin_bear = (upper_wick > body * 2) & (rng > 0)
    near_support = df.low <= support * 1.0003
    near_resistance = df.high >= resistance * 0.9997
    sig = _empty(df)
    sig[pin_bull & near_support] = "CALL"
    sig[pin_bear & near_resistance] = "PUT"
    return sig


def s04_rsi2_extreme(df):
    r = ind.rsi(df.close, 2)
    sig = _empty(df)
    sig[(r.shift(1) < 5) & (r >= r.shift(1))] = "CALL"
    sig[(r.shift(1) > 95) & (r <= r.shift(1))] = "PUT"
    return sig


def s05_stochastic_fast(df):
    k, d = ind.stochastic(df.high, df.low, df.close, 5, 3, 3)
    cross_up = (k > d) & (k.shift(1) <= d.shift(1)) & (k < 20)
    cross_dn = (k < d) & (k.shift(1) >= d.shift(1)) & (k > 80)
    sig = _empty(df)
    sig[cross_up] = "CALL"
    sig[cross_dn] = "PUT"
    return sig


def s06_donchian_breakout_short(df):
    upper, lower = ind.donchian_channel(df.high, df.low, 10)
    sig = _empty(df)
    sig[df.close > upper.shift(1)] = "CALL"
    sig[df.close < lower.shift(1)] = "PUT"
    return sig


def s07_engulfing_sr(df, lookback=25):
    bull_engulf = (df.close > df.open) & (df.close.shift(1) < df.open.shift(1)) & \
        (df.close >= df.open.shift(1)) & (df.open <= df.close.shift(1))
    bear_engulf = (df.close < df.open) & (df.close.shift(1) > df.open.shift(1)) & \
        (df.close <= df.open.shift(1)) & (df.open >= df.close.shift(1))
    support = df.low.rolling(lookback).min()
    resistance = df.high.rolling(lookback).max()
    sig = _empty(df)
    sig[bull_engulf & (df.low <= support * 1.0003)] = "CALL"
    sig[bear_engulf & (df.high >= resistance * 0.9997)] = "PUT"
    return sig


def s08_fibonacci_intrabar(df, lookback=20):
    hh = df.high.rolling(lookback).max()
    ll = df.low.rolling(lookback).min()
    rng = hh - ll
    level_618 = hh - rng * 0.618
    level_786 = hh - rng * 0.786
    uptrend = df.close > df.close.shift(lookback)
    downtrend = df.close < df.close.shift(lookback)
    in_zone_up = (df.close <= level_618) & (df.close >= level_786) & uptrend
    level_618_dn = ll + rng * 0.618
    level_786_dn = ll + rng * 0.786
    in_zone_dn = (df.close >= level_618_dn) & (df.close <= level_786_dn) & downtrend
    reversal_up = df.close > df.open
    reversal_dn = df.close < df.open
    sig = _empty(df)
    sig[in_zone_up & reversal_up] = "CALL"
    sig[in_zone_dn & reversal_dn] = "PUT"
    return sig


def s09_trendline_shortterm(df, lookback=15):
    lows = df.low
    highs = df.high
    slope_low = lows.rolling(lookback).apply(lambda x: np.polyfit(np.arange(len(x)), x, 1)[0], raw=True)
    slope_high = highs.rolling(lookback).apply(lambda x: np.polyfit(np.arange(len(x)), x, 1)[0], raw=True)
    proj_low = lows.shift(1) + slope_low.shift(1)
    proj_high = highs.shift(1) + slope_high.shift(1)
    touch_up = (slope_low > 0) & (df.low <= proj_low * 1.0002) & (df.close > df.open)
    touch_dn = (slope_high < 0) & (df.high >= proj_high * 0.9998) & (df.close < df.open)
    sig = _empty(df)
    sig[touch_up] = "CALL"
    sig[touch_dn] = "PUT"
    return sig


def s10_three_soldiers_crows(df, lookback=25):
    up = df.close > df.open
    dn = df.close < df.open
    three_up = up & up.shift(1) & up.shift(2) & (df.close > df.close.shift(1)) & (df.close.shift(1) > df.close.shift(2))
    three_dn = dn & dn.shift(1) & dn.shift(2) & (df.close < df.close.shift(1)) & (df.close.shift(1) < df.close.shift(2))
    support = df.low.rolling(lookback).min()
    resistance = df.high.rolling(lookback).max()
    sig = _empty(df)
    sig[three_up & (df.low.shift(2) <= support.shift(2) * 1.001)] = "CALL"
    sig[three_dn & (df.high.shift(2) >= resistance.shift(2) * 0.999)] = "PUT"
    return sig


def s11_macd_momentum_fast(df):
    macd_line, signal_line, hist = ind.macd(df.close, 6, 13, 5)
    cross_up = (hist > 0) & (hist.shift(1) <= 0)
    cross_dn = (hist < 0) & (hist.shift(1) >= 0)
    sig = _empty(df)
    sig[cross_up] = "CALL"
    sig[cross_dn] = "PUT"
    return sig


def s12_round_numbers(df, step=0.0050, tol=0.0004):
    nearest = (df.close / step).round() * step
    dist = (df.close - nearest).abs()
    near_level = dist <= tol
    upper_wick = df.high - df[["open", "close"]].max(axis=1)
    lower_wick = df[["open", "close"]].min(axis=1) - df.low
    body = (df.close - df.open).abs()
    exhaustion_up = lower_wick > body
    exhaustion_dn = upper_wick > body
    above = df.close > nearest
    below = df.close < nearest
    sig = _empty(df)
    sig[near_level & below & exhaustion_up] = "CALL"
    sig[near_level & above & exhaustion_dn] = "PUT"
    return sig


def s13_cci_extreme(df):
    c = ind.cci(df.high, df.low, df.close, 14)
    sig = _empty(df)
    sig[(c.shift(1) < -100) & (c >= -100)] = "CALL"
    sig[(c.shift(1) > 100) & (c <= 100)] = "PUT"
    return sig


def s14_inside_bar_breakout(df):
    inside = (df.high.shift(1) < df.high.shift(2)) & (df.low.shift(1) > df.low.shift(2))
    breakout_up = inside & (df.close > df.high.shift(1))
    breakout_dn = inside & (df.close < df.low.shift(1))
    sig = _empty(df)
    sig[breakout_up] = "CALL"
    sig[breakout_dn] = "PUT"
    return sig


def s15_volume_spike(df):
    if "volume" not in df.columns:
        return _empty(df)
    avg_vol = df.volume.rolling(20).mean()
    spike = df.volume > avg_vol * 2
    strong_up = spike & (df.close > df.open) & (df.close > df.close.shift(1))
    strong_dn = spike & (df.close < df.open) & (df.close < df.close.shift(1))
    sig = _empty(df)
    sig[strong_up] = "CALL"
    sig[strong_dn] = "PUT"
    return sig


def s16_adx_psar(df):
    a = ind.adx(df.high, df.low, df.close, 14)
    sar = ind.parabolic_sar(df.high, df.low, 0.02, 0.2)
    flip_up = (sar < df.close) & (sar.shift(1) >= df.close.shift(1))
    flip_dn = (sar > df.close) & (sar.shift(1) <= df.close.shift(1))
    sig = _empty(df)
    sig[flip_up & (a > 25)] = "CALL"
    sig[flip_dn & (a > 25)] = "PUT"
    return sig


def s17_vwap_reversion(df, window=20):
    if "volume" not in df.columns:
        return _empty(df)
    vwap = ind.vwap_rolling(df.high, df.low, df.close, df.volume, window)
    std = df.close.rolling(window).std(ddof=0)
    far_below = df.close < (vwap - 2 * std)
    far_above = df.close > (vwap + 2 * std)
    reverting_up = far_below.shift(1) & (df.close > df.close.shift(1))
    reverting_dn = far_above.shift(1) & (df.close < df.close.shift(1))
    sig = _empty(df)
    sig[reverting_up] = "CALL"
    sig[reverting_dn] = "PUT"
    return sig


def s18_doji_exhaustion(df, seq=4):
    body = (df.close - df.open).abs()
    rng = (df.high - df.low).replace(0, np.nan)
    is_doji = (body / rng) < 0.1
    up_seq = (df.close.shift(1) > df.open.shift(1))
    dn_seq = (df.close.shift(1) < df.open.shift(1))
    up_run = up_seq.rolling(seq).sum() == seq
    dn_run = dn_seq.rolling(seq).sum() == seq
    sig = _empty(df)
    doji_after_up = is_doji.shift(1) & up_run.shift(1)
    doji_after_dn = is_doji.shift(1) & dn_run.shift(1)
    sig[doji_after_up & (df.close < df.open)] = "PUT"
    sig[doji_after_dn & (df.close > df.open)] = "CALL"
    return sig


def s19_linreg_channel_short(df):
    upper, mid, lower = ind.linreg_channel(df.close, 20, 2.0)
    slope_up = mid > mid.shift(3)
    slope_dn = mid < mid.shift(3)
    sig = _empty(df)
    sig[(df.close <= lower) & slope_up] = "CALL"
    sig[(df.close >= upper) & slope_dn] = "PUT"
    return sig


def s20_volatility_spike_reversion(df, atr_period=14, spike_mult=2.5):
    a = ind.atr(df.high, df.low, df.close, atr_period)
    move = (df.close - df.close.shift(1)).abs()
    spike = move.shift(1) > a.shift(1) * spike_mult
    corr_up = spike & (df.close.shift(1) < df.open.shift(1)) & (df.close > df.open)
    corr_dn = spike & (df.close.shift(1) > df.open.shift(1)) & (df.close < df.open)
    sig = _empty(df)
    sig[corr_up] = "CALL"
    sig[corr_dn] = "PUT"
    return sig


# ---------------------------------------------------------------------------
# Grupo 2 — até 15 min (índices 21-30)
# ---------------------------------------------------------------------------

def s21_ema_cross_9_21(df):
    ema9, ema21 = ind.ema(df.close, 9), ind.ema(df.close, 21)
    cross_up = (ema9 > ema21) & (ema9.shift(1) <= ema21.shift(1))
    cross_dn = (ema9 < ema21) & (ema9.shift(1) >= ema21.shift(1))
    sig = _empty(df)
    sig[cross_up] = "CALL"
    sig[cross_dn] = "PUT"
    return sig


def s22_bollinger_rsi_combo(df):
    upper, mid, lower = ind.bollinger_bands(df.close, 20, 2.0)
    r = ind.rsi(df.close, 14)
    sig = _empty(df)
    sig[(df.low <= lower) & (r < 30)] = "CALL"
    sig[(df.high >= upper) & (r > 70)] = "PUT"
    return sig


def s23_daily_sr_breakout(df, session_bars=96):
    resistance = df.high.rolling(session_bars).max().shift(1)
    support = df.low.rolling(session_bars).min().shift(1)
    breakout_up = (df.close > resistance) & (df.close.shift(1) <= resistance.shift(1))
    breakout_dn = (df.close < support) & (df.close.shift(1) >= support.shift(1))
    sig = _empty(df)
    sig[breakout_up] = "CALL"
    sig[breakout_dn] = "PUT"
    return sig


def s24_trend_adx_pullback_ema(df):
    a = ind.adx(df.high, df.low, df.close, 14)
    ema20 = ind.ema(df.close, 20)
    trending = a > 25
    uptrend = df.close > ema20
    downtrend = df.close < ema20
    pullback_up = trending & uptrend & (df.low <= ema20 * 1.0006) & (df.close > df.open)
    pullback_dn = trending & downtrend & (df.high >= ema20 * 0.9994) & (df.close < df.open)
    sig = _empty(df)
    sig[pullback_up] = "CALL"
    sig[pullback_dn] = "PUT"
    return sig


def s25_keltner_reversion(df):
    upper, mid, lower = ind.keltner_channel(df.high, df.low, df.close, 20, 2.0)
    back_inside_up = (df.low.shift(1) <= lower.shift(1)) & (df.close > lower)
    back_inside_dn = (df.high.shift(1) >= upper.shift(1)) & (df.close < upper)
    sig = _empty(df)
    sig[back_inside_up] = "CALL"
    sig[back_inside_dn] = "PUT"
    return sig


def s26_head_shoulders_short(df, order=3, lookback=40):
    highs, lows = ind.swing_highs_lows(df.high, df.low, order)
    sig = _empty(df)
    pivot_idx = df.index[highs | lows]
    for i in range(len(df)):
        if i < lookback:
            continue
        window_piv = [p for p in pivot_idx if df.index.get_loc(p) < i and df.index.get_loc(p) >= i - lookback]
        top_piv = [p for p in window_piv if highs.loc[p]]
        if len(top_piv) >= 3:
            last3 = top_piv[-3:]
            l, c, r = (df.high.loc[p] for p in last3)
            if c > l and c > r and abs(l - r) / c < 0.002:
                neckline = min(df.low.loc[last3[0]:last3[2]])
                if df.close.iloc[i] < neckline:
                    sig.iloc[i] = "PUT"
        bot_piv = [p for p in window_piv if lows.loc[p]]
        if len(bot_piv) >= 3:
            last3 = bot_piv[-3:]
            l, c, r = (df.low.loc[p] for p in last3)
            if c < l and c < r and abs(l - r) / c < 0.002:
                neckline = max(df.high.loc[last3[0]:last3[2]])
                if df.close.iloc[i] > neckline:
                    sig.iloc[i] = "CALL"
    return sig


def s27_ichimoku_simplified(df):
    tenkan, kijun, span_a, span_b = ind.ichimoku(df.high, df.low, 9, 26, 52)
    cloud_top = pd.concat([span_a, span_b], axis=1).max(axis=1)
    cloud_bottom = pd.concat([span_a, span_b], axis=1).min(axis=1)
    above_cloud = df.close > cloud_top
    below_cloud = df.close < cloud_bottom
    cross_up = (tenkan > kijun) & (tenkan.shift(1) <= kijun.shift(1))
    cross_dn = (tenkan < kijun) & (tenkan.shift(1) >= kijun.shift(1))
    sig = _empty(df)
    sig[above_cloud & cross_up] = "CALL"
    sig[below_cloud & cross_dn] = "PUT"
    return sig


def s28_structure_hh_hl(df, order=3, lookback=30):
    highs, lows = ind.swing_highs_lows(df.high, df.low, order)
    sig = _empty(df)
    high_vals = df.high.where(highs)
    low_vals = df.low.where(lows)
    last_high = high_vals.ffill()
    prev_high = high_vals.ffill().shift(1)
    last_low = low_vals.ffill()
    prev_low = low_vals.ffill().shift(1)
    uptrend_structure = (last_high > prev_high) & (last_low > prev_low)
    downtrend_structure = (last_high < prev_high) & (last_low < prev_low)
    breakout_up = uptrend_structure & (df.close > last_high.shift(1))
    breakout_dn = downtrend_structure & (df.close < last_low.shift(1))
    sig[breakout_up] = "CALL"
    sig[breakout_dn] = "PUT"
    return sig


def s29_mtf_confluence(df_m1, df_m5, df_m15):
    """Requer os três timeframes já alinhados por timestamp (reindex/ffill)."""
    ema15 = ind.ema(df_m15.close, 20)
    ema5 = ind.ema(df_m5.close, 20)
    trend_m15 = np.where(df_m15.close > ema15, 1, -1)
    trend_m5 = np.where(df_m5.close > ema5, 1, -1)

    trend_m15_aligned = pd.Series(trend_m15, index=df_m15.index).reindex(df_m1.index, method="ffill")
    trend_m5_aligned = pd.Series(trend_m5, index=df_m5.index).reindex(df_m1.index, method="ffill")

    ema9_m1, ema21_m1 = ind.ema(df_m1.close, 9), ind.ema(df_m1.close, 21)
    cross_up = (ema9_m1 > ema21_m1) & (ema9_m1.shift(1) <= ema21_m1.shift(1))
    cross_dn = (ema9_m1 < ema21_m1) & (ema9_m1.shift(1) >= ema21_m1.shift(1))

    sig = _empty(df_m1)
    aligned_up = (trend_m15_aligned == 1) & (trend_m5_aligned == 1) & cross_up
    aligned_dn = (trend_m15_aligned == -1) & (trend_m5_aligned == -1) & cross_dn
    sig[aligned_up] = "CALL"
    sig[aligned_dn] = "PUT"
    return sig


def s30_dynamic_sr_sma(df):
    sma50, sma100 = ind.sma(df.close, 50), ind.sma(df.close, 100)
    uptrend = sma50 > sma100
    downtrend = sma50 < sma100
    touch_50_up = uptrend & (df.low.shift(1) <= sma50.shift(1)) & (df.close > df.open)
    touch_50_dn = downtrend & (df.high.shift(1) >= sma50.shift(1)) & (df.close < df.open)
    sig = _empty(df)
    sig[touch_50_up] = "CALL"
    sig[touch_50_dn] = "PUT"
    return sig


# Registro central: nome legível, função, timeframe recomendado (pandas resample) e expiração em nº de velas
STRATEGIES = {
    "01_bollinger_reversal": (s01_bollinger_reversal, "1min", 2),
    "02_ema_cross_fast": (s02_ema_cross_fast, "1min", 2),
    "03_pinbar_sr": (s03_pinbar_sr, "1min", 2),
    "04_rsi2_extreme": (s04_rsi2_extreme, "1min", 1),
    "05_stochastic_fast": (s05_stochastic_fast, "1min", 2),
    "06_donchian_breakout_short": (s06_donchian_breakout_short, "1min", 3),
    "07_engulfing_sr": (s07_engulfing_sr, "1min", 2),
    "08_fibonacci_intrabar": (s08_fibonacci_intrabar, "1min", 2),
    "09_trendline_shortterm": (s09_trendline_shortterm, "1min", 1),
    "10_three_soldiers_crows": (s10_three_soldiers_crows, "1min", 2),
    "11_macd_momentum_fast": (s11_macd_momentum_fast, "1min", 2),
    "12_round_numbers": (s12_round_numbers, "1min", 1),
    "13_cci_extreme": (s13_cci_extreme, "1min", 2),
    "14_inside_bar_breakout": (s14_inside_bar_breakout, "1min", 2),
    "15_volume_spike": (s15_volume_spike, "1min", 1),
    "16_adx_psar": (s16_adx_psar, "1min", 2),
    "17_vwap_reversion": (s17_vwap_reversion, "1min", 1),
    "18_doji_exhaustion": (s18_doji_exhaustion, "1min", 2),
    "19_linreg_channel_short": (s19_linreg_channel_short, "1min", 2),
    "20_volatility_spike_reversion": (s20_volatility_spike_reversion, "1min", 1),
    "21_ema_cross_9_21": (s21_ema_cross_9_21, "5min", 3),
    "22_bollinger_rsi_combo": (s22_bollinger_rsi_combo, "5min", 3),
    "23_daily_sr_breakout": (s23_daily_sr_breakout, "15min", 1),
    "24_trend_adx_pullback_ema": (s24_trend_adx_pullback_ema, "5min", 3),
    "25_keltner_reversion": (s25_keltner_reversion, "15min", 1),
    "26_head_shoulders_short": (s26_head_shoulders_short, "5min", 3),
    "27_ichimoku_simplified": (s27_ichimoku_simplified, "15min", 1),
    "28_structure_hh_hl": (s28_structure_hh_hl, "5min", 3),
    "30_dynamic_sr_sma": (s30_dynamic_sr_sma, "15min", 1),
}
