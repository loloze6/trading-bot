"""Kraken Futures for live runs: completed candles, the account's value and position.

Business: live decisions must use the same kind of candles as the backtest, and the real book is read from the
exchange. Kraken Futures linear perpetuals only (`PF_...`, quoted and settled in USD, 1 contract = 1 coin): the book's
USD arithmetic fits them; the inverse ones (`PI_...`, settled in the coin) do not.

Why this can't leak: a candle is kept only once its whole period has passed on the clock given (`now`); the
candle Kraken is still forming is dropped.

Keys come from two environment variables and are never logged or written anywhere.
"""
from __future__ import annotations

import os
import time

import pandas as pd

KEY_VAR, SECRET_VAR = "KRAKEN_FUTURES_API_KEY", "KRAKEN_FUTURES_API_SECRET"
REAL_HOST = "futures.kraken.com"
TIMEFRAMES = {60: "1m", 300: "5m", 900: "15m", 1800: "30m", 3600: "1h", 14400: "4h", 43200: "12h", 86400: "1d"}
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def keys_present() -> bool:
    return bool(os.environ.get(KEY_VAR)) and bool(os.environ.get(SECRET_VAR))


def make_exchange(target: str = "real", test_host: str | None = None, with_keys: bool = True):
    """A ccxt Kraken Futures client. target 'real' = futures.kraken.com; 'test' = the host Kraken gives for its
    test environment (its public demo was decommissioned on 2026-07-14, so there is no default)."""
    import ccxt
    import truststore
    truststore.inject_into_ssl()   # this PC's HTTPS needs the Windows certificate store
    ex = ccxt.krakenfutures({"enableRateLimit": True})
    if target == "test":
        if not test_host:
            raise ValueError("target 'test' needs test_host: Kraken's public demo is retired; put the host Kraken "
                             "gave you in live_config.json")
        ex.urls["api"] = {k: v.replace(REAL_HOST, test_host) for k, v in ex.urls["api"].items()}
    elif target != "real":
        raise ValueError(f"target must be 'real' or 'test', not {target!r}")
    if with_keys and keys_present():
        ex.apiKey, ex.secret = os.environ[KEY_VAR], os.environ[SECRET_VAR]
    return ex


def ccxt_symbol(symbol: str) -> str:
    """The research's coin name (BTCUSD) -> ccxt's linear perpetual (BTC/USD:USD -> Kraken PF_XBTUSD)."""
    if not symbol.endswith("USD") or len(symbol) <= 3:
        raise ValueError(f"symbol must be <COIN>USD, e.g. BTCUSD, not {symbol!r}")
    return f"{symbol[:-3]}/USD:USD"


def instrument_id(ex, symbol: str) -> str:
    ex.load_markets()
    market = ex.markets.get(ccxt_symbol(symbol))
    if market is None or not market.get("linear"):
        raise ValueError(f"{symbol}: no linear perpetual on Kraken Futures")
    return market["id"]


def fetch_completed_candles(ex, symbol: str, interval_seconds: int, since: pd.Timestamp,
                            now: pd.Timestamp) -> pd.DataFrame:
    """Candles of `interval_seconds` starting at or after `since` whose period has fully passed at `now`.
    Timestamps are the candle's start, naive UTC (the backtest's convention). Pages through Kraken's 2000-row limit."""
    tf = TIMEFRAMES.get(interval_seconds)
    if tf is None:
        raise ValueError(f"no Kraken candle size of {interval_seconds} s; one of {sorted(TIMEFRAMES)}")
    step_ms = interval_seconds * 1000
    since_ms, now_ms = _ms(since), _ms(now)
    rows, cursor = [], since_ms
    while cursor + step_ms <= now_ms:
        page = ex.fetch_ohlcv(ccxt_symbol(symbol), tf, since=cursor, limit=2000)
        page = [r for r in page if r[0] >= cursor]
        if not page:
            break
        rows += page
        cursor = page[-1][0] + step_ms
    df = pd.DataFrame(rows, columns=COLUMNS).drop_duplicates("timestamp")
    df = df[(df["timestamp"] >= since_ms) & (df["timestamp"] + step_ms <= now_ms)]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df.sort_values("timestamp").reset_index(drop=True)


def account_snapshot(ex, symbol: str) -> dict:
    """The real account: its value in USD (Kraken's 'portfolioValue' of the multi-collateral account: collateral
    plus unrealised profit and funding) and the signed position in coins on this symbol's perpetual."""
    accounts = ex.privateGetAccounts()["accounts"]
    value = float(accounts["flex"]["portfolioValue"])
    pid = instrument_id(ex, symbol).lower()
    position = 0.0
    for p in ex.privateGetOpenpositions().get("openPositions", []):
        if str(p.get("symbol", "")).lower() == pid:
            size = float(p["size"])
            position += size if p.get("side") == "long" else -size
    return {"value": value, "position": position}


def _ms(ts) -> int:
    ts = pd.Timestamp(ts)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    return int(ts.value // 1_000_000)


def utc_now() -> pd.Timestamp:
    return pd.Timestamp(time.time(), unit="s")
