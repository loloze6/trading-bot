# Data layer — architecture reference

## File map

```
data/
  data_manager.py              ← core orchestration
  feed_registry.py             ← auto-discovery of all fetchers
  fetchers/
    __init__.py                ← convenience imports
    base_fetcher.py            ← shared fetcher logic (abstract)
    ccxt_fetcher.py            ← price data (OHLCV)
    fear_greed_fetcher.py      ← example auxiliary feed (global)
    funding_rate_fetcher.py    ← example auxiliary feed (per-symbol)
```

---

## Two distinct data paths

Price data and auxiliary feeds are intentionally handled differently.
This asymmetry is by design, not an oversight.

```
PRICE DATA (OHLCV)                    AUXILIARY FEEDS
──────────────────                    ───────────────
DataManager.fetch_historical_data()   DataManager.register_feed()
  → CcxtFetcher                         → YourFetcher
    → BaseFetcher (storage/gaps)          → BaseFetcher (storage/gaps)
      → feeds CandleBuilder tick-by-tick    → pre-merged as extra columns
        → drives candle aggregation           → attached at candle close
```

**Why price data is special:** it drives `CandleBuilder` tick-by-tick and
is the engine of candle aggregation. It cannot go through `register_feed()`
because it is not a passive column — it is the heartbeat of the whole system.

**Why auxiliary feeds are different:** they are scalar values (one number per
timestamp) that are forward-filled onto candles via `merge_asof`. They add
information but do not drive the simulation.

Both paths share `BaseFetcher` for storage, gap detection, and caching.

**A third, separate consumer exists outside this directory.**
`strategy-research/tools/prescreen_signal.py::_merge_aux_feeds()` is a
simplified, standalone aux-feed loader for the cheap-IC prescreen tool — it
does not go through `DataManager.register_feed()` and is driven by a config's
`"aux_feeds": [...]` list instead of `FEED_REGISTRY`. It shares this
directory's deny-by-default philosophy (see `ADDING_A_FEED.md` Step 5, added
dispatch W14): an unrecognized feed name raises rather than being silently
dropped. It is a separate implementation, not a thin wrapper over this one —
adding a feed here does not make it available there.

---

## File-by-file summary

### `data_manager.py` 🔴 DO NOT MODIFY
The central orchestration layer. Contains:
- **`PriceTick`** and **`Candle`** — core data structures consumed everywhere
- **`CandleBuilder`** — the single candle aggregation engine shared by live
  and backtest. All tick-to-candle logic lives here and nowhere else.
- **`AuxFeedConfig`** — descriptor holding one registered auxiliary feed
  (fetcher instance, column name, aggregation function, live cached value)
- **`DataManager`** — unified live/backtest manager. Owns `CandleBuilder`,
  manages cursors, drives the simulation loop, merges auxiliary feeds into
  candle history at close, and exposes the public interface consumed by
  `TradingBot` and `BacktestEngine`

---

### `feed_registry.py` 🔴 DO NOT MODIFY DIRECTLY
Auto-discovers all `BaseFetcher` subclasses from `data/fetchers/` using
naming conventions. Adding a new fetcher file automatically makes it
available — no manual registration needed.

Naming convention: `FundingRateFetcher` → `'funding_rate'`,
`FearGreedFetcher` → `'fear_greed'`, `OpenInterestFetcher` → `'open_interest'`.

---

### `fetchers/base_fetcher.py` 🔴 DO NOT MODIFY
The abstract parent class for all fetchers. Contains all shared logic:
local CSV storage, gap detection, incremental fetching, deduplication,
date-window filtering, continuity validation. Only touch to fix a bug
that affects all fetchers equally.

---

### `fetchers/ccxt_fetcher.py` 🔴 DO NOT MODIFY
Concrete fetcher for exchange OHLCV price data via CCXT (Binance spot).
Consumed exclusively via `DataManager.fetch_historical_data()` — not
via `register_feed()`. Also exports `HistoricalDataFetcher` as a
backward-compatibility alias.

---

### `fetchers/fear_greed_fetcher.py` ✅ TEMPLATE — global feed
Fetches the daily Crypto Fear & Greed Index from Alternative.me.
Use as template for any feed that produces one global value per timestamp
(macro, sentiment). See `ADDING_A_FEED.md` for instructions.

---

### `fetchers/funding_rate_fetcher.py` ✅ TEMPLATE — per-symbol feed
Fetches Binance perpetual futures funding rates every 8h.
Use as template for any feed that produces one value per symbol per
timestamp (market structure, on-chain). See `ADDING_A_FEED.md` for instructions.

---

### `fetchers/__init__.py` 🟡 ADD IMPORT WHEN ADDING A FEED
Re-exports all fetchers. Add your new class here after creating the file.

---

## Modification rules at a glance

| File | Modify? | Why |
|---|---|---|
| `data_manager.py` | 🔴 No | Core pipeline — break it and everything breaks |
| `feed_registry.py` | 🔴 No | Auto-discovers fetchers by convention |
| `base_fetcher.py` | 🔴 No | Shared logic — changes affect all fetchers |
| `ccxt_fetcher.py` | 🔴 No | Price data pipeline — format is load-bearing |
| `fear_greed_fetcher.py` | ✅ Template | Copy for new global/macro/sentiment feed |
| `funding_rate_fetcher.py` | ✅ Template | Copy for new per-symbol market-structure feed |
| `fetchers/__init__.py` | 🟡 Add imports only | Register new fetchers here |