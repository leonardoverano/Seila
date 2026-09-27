"""Baixa e decodifica ticks históricos gratuitos da Dukascopy.

Formato do feed público (sem autenticação):
  https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YYYY}/{MM0}/{DD}/{HH}h_ticks.bi5

- MM0 é o mês indexado em 0 (janeiro = "00").
- Cada arquivo .bi5 é um bloco LZMA; quando descomprimido, contém registros
  binários de 20 bytes: (time_ms_offset, ask, bid, ask_vol, bid_vol) em
  big-endian (formato struct ">3i2f").
- Preços vêm multiplicados pelo "point value" do par (10**5 para a maioria
  dos pares, 10**3 para pares com JPY).
- Horas/dias sem negociação retornam arquivo vazio (0 bytes) — tratado como
  "sem ticks", não como erro.
"""

from __future__ import annotations

import datetime as dt
import lzma
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

BASE_URL = "https://datafeed.dukascopy.com/datafeed"

POINT_VALUE = {
    "JPY": 10**3,
}
DEFAULT_POINT_VALUE = 10**5

CACHE_DIR = Path(__file__).parent / "data_cache"
CACHE_DIR.mkdir(exist_ok=True)

RECORD = struct.Struct(">3i2f")


def _point_value(symbol: str) -> int:
    return POINT_VALUE.get(symbol[3:6].upper(), DEFAULT_POINT_VALUE)


def _hour_url(symbol: str, day: dt.date, hour: int) -> str:
    return f"{BASE_URL}/{symbol.upper()}/{day.year:04d}/{day.month - 1:02d}/{day.day:02d}/{hour:02d}h_ticks.bi5"


def _fetch_hour(symbol: str, day: dt.date, hour: int, retries: int = 10, base_delay: float = 2.0) -> bytes:
    url = _hour_url(symbol, day, hour)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            time.sleep(base_delay)
            return data
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                time.sleep(base_delay)
                return b""
            if exc.code == 429:
                wait = min(base_delay * (2**attempt), 60)
                time.sleep(wait)
                continue
            if attempt == retries - 1:
                raise
            time.sleep(base_delay * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == retries - 1:
                raise
            time.sleep(base_delay * (attempt + 1))
    return b""


def _decode_hour(raw: bytes, day: dt.date, hour: int, point_value: int) -> pd.DataFrame:
    if not raw:
        return pd.DataFrame(columns=["timestamp", "bid", "ask"])
    try:
        blob = lzma.decompress(raw)
    except lzma.LZMAError:
        return pd.DataFrame(columns=["timestamp", "bid", "ask"])

    n = len(blob) // RECORD.size
    rows = RECORD.iter_unpack(blob[: n * RECORD.size])
    base = dt.datetime(day.year, day.month, day.day, hour, tzinfo=dt.timezone.utc)

    ms_offsets = np.empty(n, dtype=np.int64)
    bids = np.empty(n, dtype=np.float64)
    asks = np.empty(n, dtype=np.float64)
    for i, (ms, ask, bid, _ask_vol, _bid_vol) in enumerate(rows):
        ms_offsets[i] = ms
        asks[i] = ask / point_value
        bids[i] = bid / point_value

    timestamps = base + pd.to_timedelta(ms_offsets, unit="ms")
    return pd.DataFrame({"timestamp": timestamps, "bid": bids, "ask": asks})


def download_ticks(symbol: str, start: dt.date, end: dt.date, use_cache: bool = True) -> pd.DataFrame:
    """Baixa ticks de `start` até `end` (inclusive), dia a dia, com cache local em parquet."""
    symbol = symbol.upper()
    point_value = _point_value(symbol)
    frames = []

    day = start
    while day <= end:
        cache_file = CACHE_DIR / f"{symbol}_{day.isoformat()}.pkl"
        if use_cache and cache_file.exists():
            frames.append(pd.read_pickle(cache_file))
            day += dt.timedelta(days=1)
            continue

        day_frames = []
        for hour in range(24):
            raw = _fetch_hour(symbol, day, hour)
            df_hour = _decode_hour(raw, day, hour, point_value)
            if not df_hour.empty:
                day_frames.append(df_hour)

        day_df = (
            pd.concat(day_frames, ignore_index=True)
            if day_frames
            else pd.DataFrame(columns=["timestamp", "bid", "ask"])
        )
        if use_cache:
            day_df.to_pickle(cache_file)
        frames.append(day_df)
        day += dt.timedelta(days=1)

    if not frames:
        return pd.DataFrame(columns=["timestamp", "bid", "ask", "mid"])

    ticks = pd.concat(frames, ignore_index=True)
    if ticks.empty:
        ticks["mid"] = []
        return ticks
    ticks["mid"] = (ticks["bid"] + ticks["ask"]) / 2
    ticks = ticks.sort_values("timestamp").reset_index(drop=True)
    return ticks


def ticks_to_ohlc(ticks: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Agrega ticks em candles OHLC. `timeframe` no formato pandas (ex.: '1s', '1min', '5min', '15min').

    `volume` é o número de ticks no candle (proxy de atividade de mercado; a
    Dukascopy não fornece volume real de contratos em ticks de Forex).
    """
    if ticks.empty:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
    indexed = ticks.set_index("timestamp")
    ohlc = indexed["mid"].resample(timeframe).ohlc()
    ohlc["volume"] = indexed["mid"].resample(timeframe).count()
    ohlc = ohlc.dropna(subset=["open", "high", "low", "close"], how="all")
    return ohlc


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Baixa ticks Dukascopy e gera candles OHLC")
    parser.add_argument("symbol", help="Ex.: EURUSD")
    parser.add_argument("start", help="YYYY-MM-DD")
    parser.add_argument("end", help="YYYY-MM-DD")
    parser.add_argument("--timeframe", default="1min")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)
    ticks = download_ticks(args.symbol, start, end)
    print(f"Ticks baixados: {len(ticks)}")
    ohlc = ticks_to_ohlc(ticks, args.timeframe)
    print(f"Candles gerados ({args.timeframe}): {len(ohlc)}")
    out = args.out or f"{args.symbol}_{args.start}_{args.end}_{args.timeframe}.csv"
    ohlc.to_csv(out)
    print(f"Salvo em {out}")
