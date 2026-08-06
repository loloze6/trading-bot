# Recon: Inventory and Structure of the Downloaded Kraken Bulk Archive

**Model:** Claude Sonnet 4.6 (recon, read-only)
**Date:** 2026-07-21
**Precondition manifest:** HEAD = `11086bb` at start (matches expected), `git status --porcelain` empty, `trading-bot/local_data/Kraken_batch/` exists and is non-empty. All confirmed before any other step.
**Status:** read-only recon only. No ingestion code written, nothing committed.

---

## 1. `.gitignore` status — not a blocker

Repo-root `.gitignore` line 39: `local_data/` (no leading slash, so it matches `local_data/` at any depth, including `trading-bot/local_data/`). Confirmed via `git check-ignore -v` against a sample file inside `Kraken_batch/master_q4/`:

```
.gitignore:39:local_data/    local_data/Kraken_batch/master_q4/ETHXBT_5.csv
```

`git ls-files local_data/Kraken_batch/` returns zero entries. The 26 GB archive is not staged, not tracked, and cannot be accidentally committed via `git add -A` etc.

One adjacent observation, not a blocker: `local_data/` itself is **not fully clean** — 3 files are already tracked despite the ignore rule (`local_data/BTCUSDT_1h.csv`, `local_data/BTCUSDT_funding_8h.csv`, `local_data/fear_greed_daily.csv`), presumably added before the ignore rule existed or via `git add -f`. Unrelated to Kraken_batch (which has nothing tracked), but worth knowing this pattern exists in the repo's history if a future `git add -A` is ever run carelessly in that directory.

## 2. Archive inventory

| | |
|---|---|
| Total files | 24,055 (all files under `Kraken_batch/`) |
| Total size on disk | 26 GB |
| Structure | `Kraken_batch/master_q4/` (12,027 data files) + `Kraken_batch/__MACOSX/master_q4/` (12,028 macOS resource-fork junk files, `._*` prefix — artifacts of an unzip on macOS, safe to ignore/delete, not data) |

**Naming convention:** `{TICKER}_{RESOLUTION_MINUTES}.csv`, flat inside `master_q4/`. Kraken uses its own base-currency tickers, not the market-standard ones — notably `XBT` for Bitcoin and `XDG` for Dogecoin (legacy Kraken codes), not `BTC`/`DOGE`. Quote currencies observed: `USD`, `USDT`, `USDC`, `EUR`, `EURC`, `EUROP`, `GBP`, `CAD`, `AUD`, `CHF`, `JPY`, `AED`, `DAI`, `PYUSD`, and cross pairs quoted in another crypto (`XBT`, `ETH`).

Representative sample: `RBCEUR_15.csv`, `ETHXBT_5.csv`, `MATICUSD_1440.csv`, `XBTUSDT_5.csv`, `XRPRLUSD_5.csv`.

Resolutions present (minutes) and file counts: `1` (1522), `5` (1521), `15` (1521), `30` (1403), `60` (1521), `240` (1496), `720` (1521), `1440` (1521). Plus one outlier: `BTCUSD_Daily_OHLC.csv` — a differently-named, likely hand-added daily file using the market-standard `BTC` ticker instead of Kraken's `XBT` convention. Not part of the standard bulk-export naming pattern; flagging so it isn't mistaken for a second BTC data source with different provenance.

## 3. 20-pair target list — mapping against the archive

Cross-referenced against `strategy-research/docs/session_reports/20260721_breadth_download_recon.md`'s ranked pair table. All USD-quoted base pairs found except one:

| # | Target | Kraken ticker | Found in archive? | Notes |
|---|---|---|---|---|
| 1 | BTC | `XBT` | Yes | `XBTUSD_*`, `XBTEUR_*`, `XBTUSDT_*`, `XBTUSDC_*`, etc. — full resolution set |
| 2 | ETH | `ETH` | Yes | `ETHUSD_*` + wide quote coverage |
| 3 | XRP | `XRP` | Yes | `XRPUSD_*`, `XRPXBT_*`, etc. |
| 4 | SOL | `SOL` | Yes | `SOLUSD_*` (note: `SOLV*` files are a different asset, not a SOL variant — don't conflate) |
| 5 | ADA | `ADA` | Yes | `ADAUSD_*` |
| 6 | SUI | `SUI` | Yes | `SUIUSD_*` (USD/EUR/GBP only, no XBT/ETH cross) |
| 7 | ZEC | `ZEC` | Yes | `ZECUSD_*`, `ZECXBT_*` |
| 8 | DOGE | `XDG` | Yes | `XDGUSD_*`, `XDGXBT_*`, etc. — **not** `DOGEUSD` (only `DOGEEUR_*` exists under the literal `DOGE` prefix, and only at EUR quote — the real DOGE liquidity is under `XDG`) |
| 9 | HYPE | — | **No** | Zero files matching `HYPE` anywhere in the archive. The companion recon doc lists HYPE/USD as Kraken's #9 pair by 24h volume, so this is a real gap, not a naming mismatch — confirmed no alternate ticker exists for it. |
| 10 | XMR | `XMR` | Yes | `XMRUSD_*`, `XMRUSDT_*`, `XMRXBT_*` |
| 11 | LTC | `LTC` | Yes | `LTCUSD_*` |
| 12 | ONDO | `ONDO` | Yes | `ONDOUSD_*` |
| 13 | NEAR | `NEAR` | Yes | `NEARUSD_*` |
| 14 | LINK | `LINK` | Yes | `LINKUSD_*` |
| 15 | TAO | `TAO` | Yes | `TAOUSD_*` |
| 16 | AVAX | `AVAX` | Yes | `AVAXUSD_*` |
| 17 | TRX | `TRX` | Yes | `TRXUSD_*` |
| 18 | AAVE | `AAVE` | Yes | `AAVEUSD_*` |
| 19 | INJ | `INJ` | Yes | `INJUSD_*` |
| 20 | UNI | `UNI` | Yes | `UNIUSD_*` (careful: `UNITEUSD_*`/`UNITEEUR_*` files are a **different** asset, "UNITE" — do not substring-match `UNI` without a boundary) |

**19/20 found, 1 missing (HYPE).** DOGE requires remapping to `XDG` (already anticipated in the companion recon doc). Two near-miss ticker collisions to guard against in any ingestion regex: `SOLV*` vs `SOL*`, and `UNITE*` vs `UNI*`.

## 4. 5-pair pilot schema (BTC/XBT, ETH, SOL, ADA, LINK) — finest resolution (1-minute)

Read `XBTUSD_1.csv`, `ETHUSD_1.csv`, `SOLUSD_1.csv`, `ADAUSD_1.csv`, `LINKUSD_1.csv` directly.

**Schema:** No header row in any file. 7 comma-separated columns:

```
unix_timestamp, open, high, low, close, volume, trade_count
```

Column order confirmed by value sanity, not just assumption — e.g. `XBTUSD_1.csv` row `1381201080,123.91,123.91,123.9,123.9,1.9916,2`: `high(123.91) >= open,close(123.91,123.9) >= low(123.9)` holds on every sampled row, consistent with standard OHLC ordering and inconsistent with any other column permutation.

**Timestamp format:** Unix **seconds**, not milliseconds — first `XBTUSD` row is `1381095240`, which converts to `2013-10-06 21:34:00`, a plausible Kraken BTC/USD launch-era timestamp; a millisecond interpretation would place it in 1970. 10-digit values throughout confirm seconds.

**Timezone:** UTC. Not stated in-file (no header, no metadata) — this is inferred from Kraken's own API convention (all Kraken REST/WS endpoints, including the historical OHLC endpoint this bulk export is drawn from, return Unix epoch timestamps that are UTC-referenced by definition/documentation) combined with the observed fact that every one of the 5 pilot files ends at exactly `1767225540` / `1767225480` = `2025-12-31 23:59:00`/`23:58:00` UTC — a clean UTC year-end cutoff across all 5 independently-traded pairs, which is the signature of a single UTC-referenced export job cut at a UTC calendar boundary rather than 5 unrelated coincidences. Flagging this as inference from convention + corroborating evidence, not a directly-asserted fact in the files themselves — worth a spot-check against Kraken's public OHLC API for one pair/timestamp before treating it as certain if precision matters downstream.

## 5. 5-pair pilot coverage (actual, not assumed)

| Pair | File | Rows | First (UTC) | Last (UTC) |
|---|---|---|---|---|
| BTC | `XBTUSD_1.csv` | 4,636,234 | 2013-10-06 21:34:00 | 2025-12-31 23:59:00 |
| ETH | `ETHUSD_1.csv` | 4,130,951 | 2015-08-07 14:03:00 | 2025-12-31 23:59:00 |
| SOL | `SOLUSD_1.csv` | 1,969,957 | 2021-06-17 15:32:00 | 2025-12-31 23:59:00 |
| ADA | `ADAUSD_1.csv` | 2,113,118 | 2018-09-28 13:25:00 | 2025-12-31 23:59:00 |
| LINK | `LINKUSD_1.csv` | 1,731,064 | 2019-09-25 14:00:00 | 2025-12-31 23:58:00 |

All 5 terminate at the 2025 year-end boundary — this is a **static year-end export**, not a live-updating feed. Given today's date (2026-07-21), the archive has a **~7-month gap** between its last row and the present. If the eventual backtest/ingestion needs data through "now," this archive alone doesn't cover it and would need a live top-up (e.g. via the existing `CcxtFetcher`) for Jan 2026 onward. Not a defect in the archive — just a scope boundary worth being explicit about before the pilot dispatch assumes full recency.

## 6. Cache-key collision — confirmed still true

Re-read current definitions:

- `trading-bot/data/fetchers/base_fetcher.py:110-118` — abstract `cache_key(symbol)`, docstring examples are all symbol-only (`'BTCUSDT_5m'`, `'BTCUSDT_funding_8h'`), no exchange in any example.
- `trading-bot/data/fetchers/base_fetcher.py:211` — `_csv_path()`: `os.path.join(self.data_dir, f"{self.cache_key(symbol)}.csv")`. Single flat directory, filename = `cache_key(symbol) + ".csv"`.
- `trading-bot/data/fetchers/ccxt_fetcher.py:101-105` — `CcxtFetcher.cache_key()`: `return f"{symbol}_{self.ccxt_timeframe}"`. `self.exchange_id` is set in `__init__` (line 85) and is available on the instance, but is **not** referenced in `cache_key()`.

Confirmed: the collision risk is real and unchanged. A `CcxtFetcher` instance pointed at Kraken with `symbol="BTCUSDT"` and `ccxt_timeframe="1h"` would produce `cache_key() == "BTCUSDT_1h"` — identical to the existing Binance-sourced `local_data/BTCUSDT_1h.csv` already on disk and already tracked in git. Loading one would silently return the other exchange's candles.

This is somewhat masked for the actual 20-pair pull because Kraken's tickers (`XBTUSD`, `ADAUSD`, ...) mostly don't lexically match Binance's (`BTCUSDT`, `ADAUSDT`), so most pairs would land in genuinely new cache slots rather than overwriting existing ones — except **exact accidental collisions are still possible** wherever a Kraken-normalized symbol happens to match a Binance one already cached (and there's currently no mechanism that would catch it if it did; it would fail silently as a wrong-data read, not an error).

**Proposed fix shape (report only, not implemented):** qualify the cache key with the exchange, e.g. `CcxtFetcher.cache_key()` → `f"{self.exchange_id}_{symbol}_{self.ccxt_timeframe}"` (→ `kraken_XBTUSD_1h.csv` / `binance_BTCUSDT_1h.csv`), or equivalently route through an exchange-named subdirectory (`data_dir/kraken/XBTUSD_1h.csv`) if a flat namespace is not required. Either resolves the collision; the subdirectory form also makes `Kraken_batch`-sourced pilot files trivially distinguishable from live-fetched ones at a glance. Companion doc `20260721_breadth_download_recon.md` (line 84, "Note on naming convention") already flags a related but distinct issue — Kraken's `BASE/QUOTE` CCXT normalization producing keys like `BTC_USD` rather than compact `BTCUSD` — so the exchange-qualification and the symbol-normalization questions should probably be decided together in the implementation dispatch rather than separately.

## 7. Sufficiency verdict

**Sufficient to proceed with the 5-pair pilot ingestion dispatch**, with two caveats to carry forward, not blockers:

1. **BTC's canonical ticker is `XBT`, not `BTC`** — the ingestion mapping table needs this substitution hardcoded or config-driven; a naive `symbol.replace("USDT","")` style lookup will miss it.
2. **Coverage stops 2025-12-31** — if the pilot needs data through the present, a live-fetch top-up for the ~7-month gap is a separate, additional step, not covered by this archive.

All 5 pilot files are present, non-empty, share one consistent 7-column headerless schema, have internally consistent OHLC value ordering, use unix-second UTC timestamps, and have multi-year (9–12 year for BTC/ETH, 4–7 year for SOL/ADA/LINK) row-verified coverage. No malformed or truncated files encountered in the 5 pilot reads.

Separately, for the full 20-pair pull (a later dispatch, not this one): **HYPE has no data in this archive** and will need a fallback source (live `ccxt` fetch against Kraken, since HYPE/USD is confirmed actively trading there per the companion recon doc's volume ranking) before that pair can be included.
