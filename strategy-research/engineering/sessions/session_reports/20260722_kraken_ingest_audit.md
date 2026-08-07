# Independent audit — commit 32b1c13 (exchange-qualified cache key + Kraken 5-pair pilot ingestion)

**Auditor:** Claude Opus 4.8 (independent; 32b1c13 authored by Sonnet 5)
**Date:** 2026-07-22
**Mode:** READ-ONLY. No remediation. Only write made: `git checkout -- trading-bot/results/trades.json`
(pre-authorized, ledger D4).

**Evidence policy applied:** every claim below is recomputed from raw artifacts (Kraken bulk CSVs,
cache CSVs, live import of the fetcher classes) or from Kraken's own published material. The
implementer's commit message, docstrings, `20260721_kraken_archive_recon.md`, and ledger entry G1
were treated as claims under audit, never as sources.

---

## 0. Precondition manifest — PASS

```
$ git log --oneline -1
32b1c13 Phase 2 Track A: exchange-qualified cache key + Kraken 5-pair pilot ingestion
$ git status --porcelain
(empty)
```

Tree clean at start and at end of audit.

---

## Target A — Kraken bulk OHLCVT documented column order — **CONFIRMED**

### External citation

Kraken support, *"Downloadable historical OHLCVT (Open, High, Low, Close, Volume, Trades) data"*
— https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data
(retrieved 2026-07-22). Indexed under Kraken support's *CSV Data* section
(https://support.kraken.com/sections/360009899492-csv-data, retrieved 2026-07-22).

Kraken's own title defines the file's payload fields by acronym: **OHLCVT = Open, High, Low, Close,
Volume, Trades** — six fields, plus the unix timestamp. The article states each ZIP contains CSVs
for the 1/5/15/30/60/240/720/1440-minute intervals and that entries exist only for intervals in
which trades occurred.

### VWAP: present in the REST API, ABSENT from the bulk CSV

This is the exact conflation the dispatch flagged, and one of my own web-search passes fell into it
before I checked the primary source. The two schemas are different objects:

| Source | Schema |
|---|---|
| REST `OHLC` endpoint (docs.kraken.com/exchange/guides/general/historical-data, retrieved 2026-07-22) | `[time, open, high, low, close, **vwap**, volume, count]` — 8 fields |
| Bulk OHLCVT CSV export (support article above) | `timestamp, open, high, low, close, volume, trades` — 7 fields, **no vwap** |

The acronym is OHLCV**T**, not OHLCV**WT** — Kraken does not name a VWAP field in the download
product. A search-engine summary asserting "OHLCVT data includes VWAP" is quoting the REST schema
and is wrong about the CSV.

### Field-by-field comparison against `KRAKEN_RAW_COLUMNS`

`trading-bot/tools/ingest_kraken_archive.py`:

```python
KRAKEN_RAW_COLUMNS = ["unix_s", "open", "high", "low", "close", "volume", "trade_count"]
```

| # | Kraken documented | `KRAKEN_RAW_COLUMNS` | Match |
|---|---|---|---|
| 1 | Unix timestamp (seconds) | `unix_s` | ✅ |
| 2 | Open | `open` | ✅ |
| 3 | High | `high` | ✅ |
| 4 | Low | `low` | ✅ |
| 5 | Close | `close` | ✅ |
| 6 | Volume | `volume` | ✅ |
| 7 | Trades | `trade_count` | ✅ |

**Match, 7/7. No VWAP column to account for.**

### Independent empirical corroboration (does not rely on repo code or docs)

Direct structural analysis of the raw archive files themselves — 341,535 rows across the 5 pilot
pairs — decides the VWAP question on its own, without needing the documentation:

```
XBTUSD : ncols=7 rows=96381 high_viol=0 low_viol=0 tradecount_all_int=True
         col6 range [1.531e-05, 7113.42]      close range [122, 126073]      median col6/close = 6.410e-03
ETHUSD : ncols=7 rows=87690 high_viol=0 low_viol=0 tradecount_all_int=True   median col6/close = 1.563e+00
SOLUSD : ncols=7 rows=39743 high_viol=0 low_viol=0 tradecount_all_int=True   median col6/close = 9.716e+01
ADAUSD : ncols=7 rows=63291 high_viol=0 low_viol=0 tradecount_all_int=True   median col6/close = 6.122e+05
LINKUSD: ncols=7 rows=54430 high_viol=0 low_viol=0 tradecount_all_int=True   median col6/close = 5.837e+02
```

Three independent structural facts:

1. **Exactly 7 columns.** A VWAP-bearing file would have 8. There is no room for a dropped field.
2. **Column 6 is not price-scaled.** If col-6 were VWAP, `col6/close` would sit at ≈1.0 for every
   pair. Observed values span `6.4e-03` (XBT) to `6.1e+05` (ADA) — five orders of magnitude, and the
   ordering tracks each asset's unit price exactly as base-asset volume must. Decisive.
3. **OHLC ordering verified, not assumed.** Across all 341,535 rows: `high` is never below
   `max(open, close, low)` and `low` is never above `min(open, close, high)` — **0 violations**. A
   transposed O/H/L/C mapping would produce violations at scale. Column 7 is integral in every row,
   consistent with a trade count.

Sample raw row (`XBTUSD_60.csv`, last line): `1767222000,87584.2,87584.2,87500.1,87500.1,14.09024435,1299`
— col-6 `14.09` BTC volume, col-7 `1299` trades. Col-6 as VWAP would read ≈87,500.

**Verdict: CONFIRMED. Premise holds; no STOP condition triggered.**

---

## Target B — cross-venue reconciliation — **CONFIRMED**

Files read separately and never merged: `local_data/{BTCUSDT_1h.csv, ETHUSDT_1h.csv}` (Binance,
USDT-quoted) vs `local_data/{kraken_XBTUSD_1h.csv, kraken_ETHUSD_1h.csv}` (Kraken, USD-quoted).
Comparison restricted to the intersecting timestamp index.

| | BTC | ETH |
|---|---|---|
| Binance rows / span | 74,457 · 2018-01-01 → 2026-07-05 | 74,457 · 2018-01-01 → 2026-07-05 |
| Kraken rows / span | 96,381 · 2013-10-06 → 2025-12-31 | 87,690 · 2015-08-07 → 2025-12-31 |
| Overlapping bars | 69,923 · 2018-01-01 → 2025-12-31 | 69,923 · 2018-01-01 → 2025-12-31 |
| **median \|Δ close\|** | **0.0576 %** (5.8 bp) | **0.0615 %** (6.2 bp) |
| mean \|Δ\| | 0.1731 % | 0.1797 % |
| p99 \|Δ\| | 2.3789 % | 2.4168 % |
| **max \|Δ\|** | **10.1367 %** | **9.6894 %** |
| signed median Δ | **+0.0129 %** | **+0.0060 %** |
| median ratio K/B | **1.000129** | **1.000060** |

### Worst 5 divergences

**BTC**

| Timestamp | \|Δ\| | Binance (USDT) | Kraken (USD) |
|---|---|---|---|
| 2018-10-15 06:00 | 10.137 % | 7410.03 | 6658.9 |
| 2018-10-15 11:00 | 8.213 % | 6982.28 | 6408.8 |
| 2018-10-15 13:00 | 7.934 % | 6950.54 | 6399.1 |
| 2018-10-15 12:00 | 7.789 % | 6934.97 | 6394.8 |
| 2018-10-15 15:00 | 7.396 % | 6907.01 | 6396.2 |

**ETH**

| Timestamp | \|Δ\| | Binance (USDT) | Kraken (USD) |
|---|---|---|---|
| 2018-10-15 06:00 | 9.689 % | 235.00 | 212.23 |
| 2018-10-15 11:00 | 8.239 % | 221.75 | 203.48 |
| 2018-10-15 13:00 | 8.155 % | 218.27 | 200.47 |
| 2018-10-15 12:00 | 7.984 % | 218.94 | 201.46 |
| 2018-10-15 14:00 | 7.561 % | 215.84 | 199.52 |

### Pattern observed: normal cross-exchange spread. No bug signature.

The four bug signatures were tested individually and all are negative:

- **Systematic offset — ABSENT.** Signed median Δ is `+0.0129 %` (BTC) / `+0.0060 %` (ETH), i.e. an
  order of magnitude smaller than the absolute median. Errors are two-sided noise, not a bias.
- **Constant scale factor — ABSENT.** Median ratio Kraken/Binance = `1.000129` / `1.000060`. A
  units or column-mapping error would park this at a non-unit constant.
- **Fixed hourly offset (timestamp bug) — ABSENT**, by two independent tests:
  - Top-1 % divergences are uniform across hour-of-day (BTC counts per hour range 26–34 over 24
    buckets; ETH 26–33). A timezone shift would concentrate them.
  - Explicit lag sweep — shifting the Kraken series and re-measuring median \|Δ\|:

    | lag | BTC | ETH |
    |---|---|---|
    | −2 h | 0.3934 % | 0.5306 % |
    | −1 h | 0.2868 % | 0.3831 % |
    | **0 h** | **0.0576 %** | **0.0615 %** |
    | +1 h | 0.2879 % | 0.3826 % |
    | +2 h | 0.3916 % | 0.5236 % |

    Zero lag is a sharp minimum, ~5× better than ±1 h, and the curve is symmetric. Timestamp
    alignment is correct.
- **Column mapping — ABSENT.** A 5.8 bp median between two independently-sourced venues is not
  achievable under any mis-mapping.

### The 10 % tail is an economically real event, not a data defect

Every one of the top-5 divergences for **both** assets falls on **2018-10-15**, at the **same
hours**, in the **same direction** (Kraken-USD below Binance-USDT). A per-asset ingestion error
cannot produce a synchronized, same-signed, same-hour dislocation across two independently ingested
files.

That date is the Tether depeg: USDT traded down to ~$0.87–0.92 across venues on 2018-10-15
([CoinDesk, 2018-10-15](https://www.coindesk.com/markets/2018/10/15/price-of-stable-cryptocurrency-tether-tanks-to-18-month-low);
[Protos, history of Tether's peg](https://protos.com/history-of-tethers-peg-every-time-usdt-traded-above-or-below-one-dollar/);
retrieved 2026-07-22). A USDT worth $0.90 mechanically inflates a BTC/USDT quote ~11 % relative to
BTC/USD. Observed maxima are 10.14 % (BTC) and 9.69 % (ETH) — correct sign, correct magnitude,
correct date. This is the **documented USD-vs-USDT quote divergence already flagged in ledger G1**
manifesting exactly where theory predicts.

Median \|Δ\| by year also decays monotonically as both venues' liquidity matured — BTC 0.180 %
(2018) → 0.033 % (2023) → 0.034 % (2025); ETH 0.223 % → 0.032 % → 0.035 % — the signature of
genuine market microstructure, not of a static mapping error (which would be time-invariant).

**Verdict: CONFIRMED. Median 5.8 bp / 6.2 bp is well within normal cross-exchange spread and far
below the 1 % STOP threshold. This independently corroborates Target A: a wrong column mapping could
not yield 5.8 bp agreement against a second venue.**

---

## Target C — real load path & read-side timezone behaviour — **CONFIRMED**

Constructed a genuine `CcxtFetcher(exchange="kraken", data_dir=local_data/)` and loaded through
`_load_local()` and `get_data()`. Network was stubbed out (`_fetch_remote` replaced with a recording
no-op) so this measures the read path only and cannot be contaminated by a live fetch.

```
--- BTC (XBTUSD) ---
  cache_key = kraken_XBTUSD_1h
  _csv_path = kraken_XBTUSD_1h.csv exists=True
  _load_local rows=96381  dtype=datetime64[ns]  tz=None
  raw epochs n=96381 vs loaded n=96381  identical=True
    row  0: unix 1381093200 -> stdlib UTC 2013-10-06 21:00:00 | loaded 2013-10-06 21:00:00 | match=True
    row -1: unix 1767222000 -> stdlib UTC 2025-12-31 23:00:00 | loaded 2025-12-31 23:00:00 | match=True
    written timestamp string = '2013-10-06 21:00:00'  has_offset_suffix=False
    remote fetch attempts during get_data(): 0
  get_data() rows=744  (2020-01-01 → 2020-01-31 window)
    get_data timestamps all present in raw epochs: True

--- ETH (ETHUSD) ---
  cache_key = kraken_ETHUSD_1h
  _load_local rows=87690  dtype=datetime64[ns]  tz=None
  raw epochs n=87690 vs loaded n=87690  identical=True
    row  0: unix 1438956000 -> stdlib UTC 2015-08-07 14:00:00 | loaded 2015-08-07 14:00:00 | match=True
    row -1: unix 1767222000 -> stdlib UTC 2025-12-31 23:00:00 | loaded 2025-12-31 23:00:00 | match=True
    written timestamp string = '2015-08-07 14:00:00'  has_offset_suffix=False
    remote fetch attempts during get_data(): 0
  get_data() rows=744
```

The comparison is **element-wise across all 96,381 / 87,690 rows** — `pd.to_datetime(raw.unix_s,
unit="s")` vs the loaded column — not merely a first/last spot check.

### On the `pd.to_datetime(df["timestamp"])` concern (`base_fetcher.py:226`)

The missing `utc=` argument is **not** a live defect here, and the reason is concrete rather than
incidental:

- The written strings carry **no offset suffix** — verified by regex over the actual file bytes:
  `'2013-10-06 21:00:00'`, `has_offset_suffix=False`.
- With no suffix, `pd.to_datetime` returns tz-**naive** `datetime64[ns]` (confirmed: `tz=None`), and
  performs no locale conversion. The naive-UTC wall-clock convention of the Binance cache is
  preserved end to end.
- Round trip is bit-exact against the stdlib UTC recomputation from the raw epochs.

**Latent risk, not a present defect (worth a carry-forward, no code change requested):** the safety
here rests on the *writer* never emitting an offset suffix. If any future producer writes
offset-bearing or mixed-offset timestamps into this flat cache directory,
`pd.to_datetime(...)` without `utc=True` would either silently localize-and-shift or, on mixed
offsets, return an `object` column of `datetime` — and no guard downstream would catch it. The
ingester's `verify_utc_roundtrip` covers only the write side, as the dispatch anticipated.

**Verdict: CONFIRMED. Timestamps are unaltered by the load path; no STOP condition triggered.**

---

## Target D — `cache_key()` docstring collision claim — **DEFECT (documentation)**

The docstring at `trading-bot/data/fetchers/ccxt_fetcher.py:101-118` asserts:

> "The key is exchange-qualified so caches from different venues **can never collide in the flat
> data_dir namespace**"

Tested against the other `BaseFetcher` subclasses:

| Fetcher | `cache_key()` | Has `exchange_id`? | Uses it in the key? |
|---|---|---|---|
| `CcxtFetcher` (`ccxt_fetcher.py:117`) | `f"{prefix}{symbol}_{self.ccxt_timeframe}"`, `prefix = "" if exchange_id == "binance" else f"{exchange_id}_"` | yes | **yes** |
| `FundingRateFetcher` (`funding_rate_fetcher.py:106`) | `f"{symbol}_funding_8h"` | **yes — set at line 85** | **NO** |
| `FearGreedFetcher` (`fear_greed_fetcher.py:91`) | `"fear_greed_daily"` | no | n/a (single-source, venue-agnostic — genuinely cannot collide) |

**`FundingRateFetcher` sets `self.exchange_id = exchange_id` at line 85 and then ignores it in
`cache_key()` at line 106.** Two `FundingRateFetcher` instances configured for different venues —
e.g. `binance` and `bybit`, both fetching `BTCUSDT` — derive the identical cache key
`BTCUSDT_funding_8h` and therefore the identical file `local_data/BTCUSDT_funding_8h.csv`. Via
`_merge_and_store` they would interleave two venues' funding rates into one file, deduplicated on
timestamp only, with no venue column and no error. That is precisely the wrong-data-read failure
mode the commit fixed for OHLCV, still live one module over.

The docstring's claim is **scoped-true and universally-false**: accurate about `CcxtFetcher`, which
is what it fixes; inaccurate as written, because it makes an unqualified statement about "the flat
data_dir namespace" — a namespace shared with a sibling fetcher that does not honour the invariant.

Severity assessment: **latent, not currently exploited.** No current caller instantiates
`FundingRateFetcher` against a second venue, so no on-disk file is corrupt today. The defect is that
the docstring records a namespace-wide guarantee the codebase does not provide, which is exactly the
kind of claim a future author would rely on without re-verifying.

**Reported only — no fix applied, per dispatch.**

**Verdict: DEFECT (documentation overreach; latent code risk in `funding_rate_fetcher.py:106`).**

---

## Target E — `validate_data_continuity()` on all 5 pairs — **CONFIRMED**

Expected bar count computed as `floor((last − first) / 1h) + 1` over each file's own observed span.

| Pair | Rows | First | Last | Expected | Missing | Missing % | Distinct gaps | Largest gap |
|---|---|---|---|---|---|---|---|---|
| **BTC** (`XBTUSD`) | 96,381 | 2013-10-06 21:00 | 2025-12-31 23:00 | 107,259 | 10,878 | **10.14 %** | 3,262 | **2 d 09 h** — 2014-09-25 18:00 → 2014-09-28 03:00 |
| **ETH** (`ETHUSD`) | 87,690 | 2015-08-07 14:00 | 2025-12-31 23:00 | 91,186 | 3,496 | 3.83 % | 849 | 2 d 04 h — 2015-08-08 21:00 → 2015-08-11 01:00 |
| **SOL** (`SOLUSD`) | 39,743 | 2021-06-17 15:00 | 2025-12-31 23:00 | 39,801 | 58 | 0.15 % | 14 | 1 d 03 h — 2021-06-24 18:00 → 2021-06-25 21:00 |
| **ADA** (`ADAUSD`) | 63,291 | 2018-09-28 13:00 | 2025-12-31 23:00 | 63,635 | 344 | 0.54 % | 281 | 7 h — 2024-04-14 02:00 → 2024-04-14 09:00 |
| **LINK** (`LINKUSD`) | 54,430 | 2019-09-25 14:00 | 2025-12-31 23:00 | 54,946 | 516 | 0.94 % | 350 | 9 h — 2019-12-28 02:00 → 2019-12-28 11:00 |

`validate_data_continuity()` returned `continuous=False` for all five, with reported gap counts
matching my independent `diff > 1h` count exactly in every case (3,262 / 849 / 14 / 281 / 350) —
the existing validator is itself corroborated.

### On the director's BTC figure — **I agree**

Director: ~10.1 % missing, 96,381 actual vs ~107,256 expected over 2013-10-06 → 2025-12-31.
Recomputed: 96,381 actual, **107,259** expected, 10,878 missing = **10.14 %**.

The 3-bar difference in the expected count is an inclusive-endpoint convention, not a disagreement:
`(2025-12-31 23:00 − 2013-10-06 21:00) = 107,258 h`, `+1` for the inclusive first bar = 107,259.
Materially identical; **the 10.1 % figure is confirmed.**

### Gap concentration — benign, decisively

Missing bars per year:

**BTC** — `2013: 825/2,067 (39.9%) · 2014: 5,438/8,760 (62.1%) · 2015: 4,348/8,760 (49.6%) ·
2016: 182/8,784 (2.1%) · 2017: 2 (0.0%) · 2018: 51 (0.6%) · 2019: 3 · 2020: 1 · 2021: 6 · 2022: 0 ·
2023: 1 · 2024: 12 · 2025: 9`

- **2013–2015 account for 10,611 of 10,878 missing bars = 97.5 % of all gaps.**
- **2016 onward: 267 missing bars out of 87,652 = 0.30 %.**
- **2017 onward: 85 missing bars out of 78,868 = 0.11 %.**
- 2022 is perfectly complete (0 missing).

**ETH** — `2015: 2,746/3,514 (78.1%) · 2016: 612 (7.0%) · 2017: 55 (0.6%) · 2018: 50 (0.6%) ·
2019–2025: ≤12/yr`. 2015–2016 = 3,358 of 3,496 = **96.1 %** of all gaps. 2017 onward: 138 bars =
0.16 %.

**SOL / ADA / LINK** — all listing-era-front-loaded and already tiny in absolute terms:
SOL 35 of 58 in its 2021 listing year; ADA 267 of 344 in 2018–2019; LINK 483 of 516 in 2019–2020.
Every pair sits at ≤14 missing bars/yr from 2021 onward.

This matches Kraken's documented export semantics exactly — the support article states OHLCVT rows
exist only for intervals in which trades occurred, so a missing bar in the illiquid early era means
"no trades that hour," not "lost data." The pattern is a clean monotonic decay tracking each pair's
liquidity ramp.

**Assessment: gaps are overwhelmingly concentrated in the early illiquid era and are benign. For any
backtest window starting 2017-01-01 or later, BTC is 99.89 % complete and ETH 99.84 % complete. No
recent-year gap problem exists for breadth backtests.** The one caveat is mechanical, not about
gaps: a strategy backtesting BTC from 2013–2015 would be trading a 40–60 %-sparse series and should
either start later or resample.

**Verdict: CONFIRMED.**

---

## Target F — backtest reachability & ledger carry-forward — **DEFECT (documentation)**

### Code fact — confirmed

```
$ grep -n 'exchange="binance"' trading-bot/data/data_manager.py
768:            exchange="binance",
```

`data_manager.py:768` hardcodes `exchange="binance"` in the `HistoricalDataFetcher` construction. By
`cache_key()`'s own Binance-unprefixed rule, that fetcher can only ever derive keys of the form
`{symbol}_{tf}` — never `kraken_*`. **No backtest can currently reach any of the five ingested
Kraken cache files.** Correctly out of scope for 32b1c13, which touched only `ccxt_fetcher.py`,
the new tool, its tests, and the ledger (`git show --stat`: 4 files, +453/−2).

### Ledger fact — the gap is NOT documented

Ledger G1 (`strategy-research/PIPELINE_IMPROVEMENTS_20260712_v4.md:1385-1442`) ends with:

> **CARRY-FORWARD (open, NOT resolved here) for the full 20-pair scale-up:**
> 1. **HYPE is entirely missing from the archive** …
> 2. **Coverage stops 2025-12-31** … the ~7-month gap (2026-01-01 → today) needs a live-fetch
>    top-up per pair.

**The list has exactly two items. `data_manager.py:768` reachability is not among them, and the
string `data_manager` does not appear anywhere in G1.**

This is the most consequential of the three, and its omission is qualitatively different from the
other two. Carry-forwards 1 and 2 are *data-completeness* gaps — the ingested data is usable, just
not complete. The reachability gap is a *usability* gap: it makes 341,535 correctly-ingested,
independently-verified rows **completely unreachable by any consumer in the repo**. A reader of G1
would reasonably conclude the pilot data is available to backtests modulo HYPE and the 7-month tail.
It is not available at all.

Both carry-forwards that *are* listed were independently verified as accurate:
- HYPE: no `HYPE*` file in `local_data/Kraken_batch/master_q4/`.
- Coverage: every one of the 5 pairs terminates at `2025-12-31 23:00` (Target E table).

**Reported only — no fix applied, per dispatch.**

**Verdict: DEFECT (ledger G1 omits the reachability carry-forward). Code scope decision itself was
correct.**

---

## Step 8 — test suite

**Claim under audit:** 44 passed / 6 new.

Run under the project's own config (`trading-bot/pytest.ini`, `testpaths = tests`, `addopts` include
`-m "not slow"`), from `trading-bot/`:

```
collected 54 items / 10 deselected / 44 selected
================ 44 passed, 10 deselected, 3 warnings in 4.76s ================
```

New file in isolation:

```
$ python -m pytest tests/test_kraken_archive_ingest.py -q
collected 6 items
tests\test_kraken_archive_ingest.py ......                        [100%]
6 passed in 2.62s
```

**Claim CONFIRMED exactly: 44 passed, 6 new, all green.**

### Note on a wider invocation (not a defect in this commit)

Running `pytest` from the **repository root** instead ignores `trading-bot/pytest.ini`'s `testpaths`
and `-m "not slow"` marker filter, collecting the whole tree:

```
388 passed, 3 warnings, 4 errors in 94.66s
ERROR trading-bot/tests/test_regression_backtest.py::test_trade_count
ERROR trading-bot/tests/test_regression_backtest.py::test_net_pnl
ERROR trading-bot/tests/test_regression_backtest.py::test_sharpe
ERROR trading-bot/tests/test_regression_backtest.py::test_config_actually_loaded
ValueError: invalid strategy_config  (trading-bot/strategies/main_strategy.py:32)
```

These 4 are the `slow`-marked regression tests that the project config deliberately deselects; they
error on config resolution when invoked from the wrong rootdir. `32b1c13` touches none of
`main_strategy.py`, the config, or that test file, so this is **not attributable to the commit** and
I do not raise it as a finding against it. Flagging only as an observation: the 44-passed figure is
config-scoped, and the suite is not root-invocable.

### Tree hygiene

`trading-bot/results/trades.json` dirtied during the root-level run (known pattern, ledger D4).
Reverted with the pre-authorized `git checkout -- trading-bot/results/trades.json`. Final
`git status --porcelain` is **empty** apart from this untracked report. No other write was made.

---

## Verdict summary

| Target | Result | Establishing evidence |
|---|---|---|
| **A** — Kraken bulk column order | **CONFIRMED** | Kraken support "OHLCVT = Open, High, Low, Close, Volume, Trades" (retrieved 2026-07-22); 7/7 field match; **0 OHLC-ordering violations in 341,535 rows**; median col6/close spans 6.4e-03→6.1e+05 ⇒ col-6 is volume, not VWAP |
| **B** — cross-venue reconciliation | **CONFIRMED** | median \|Δclose\| **0.0576 %** BTC / **0.0615 %** ETH over 69,923 shared bars; ratio 1.000129; lag-0 is a 5× sharp minimum; 10.1 % max = 2018-10-15 Tether depeg |
| **C** — real load path | **CONFIRMED** | `_load_local` returns **96,381/87,690 rows element-wise identical** to raw epochs; `tz=None`, no offset suffix written; 0 network calls |
| **D** — cache-key collision claim | **DEFECT** (doc) | `funding_rate_fetcher.py:106` sets `exchange_id` at line 85 and **ignores it** in `cache_key()` ⇒ "can never collide" is false namespace-wide |
| **E** — continuity, 5 pairs | **CONFIRMED** | BTC **10,878/107,259 = 10.14 %** (agrees with director's ~10.1 %); **97.5 % of BTC gaps in 2013–2015**; 2017+ = 0.11 % |
| **F** — reachability carry-forward | **DEFECT** (doc) | `data_manager.py:768` hardcodes binance; ledger G1 lists **exactly 2** carry-forwards, neither being reachability |

### Overall: **RATIFY WITH CARRY-FORWARDS**

The commit's substance is sound. Target A's premise — the load-bearing one, on which every test in
`test_kraken_archive_ingest.py` would pass regardless — is independently verified against Kraken's
own published material **and** corroborated three ways from the raw bytes. Target B provides the
empirical seal: 5.8 bp median agreement against a second venue is unachievable under any column,
units, or timestamp error. The 341,535 ingested rows are correct.

No STOP condition triggered. Both defects are documentation, both are latent rather than active, and
neither impugns the ingested data.

**Carry-forwards to record:**

1. **(from F, highest priority)** Add the `data_manager.py:768` hardcoded-`exchange="binance"`
   reachability gap to ledger G1's carry-forward list. Until it is parameterized, no backtest can
   read the Kraken cache — the pilot data is verified but unreachable, which G1 currently does not
   say.
2. **(from D)** Either narrow the `cache_key()` docstring to a `CcxtFetcher`-scoped claim, or extend
   exchange qualification to `FundingRateFetcher.cache_key()` (`funding_rate_fetcher.py:106`), which
   holds `self.exchange_id` from line 85 and discards it. The claim as written is false for the
   shared namespace it names.
3. **(from C, minor/latent)** `base_fetcher.py:226` calls `pd.to_datetime(df["timestamp"])` with no
   `utc=`. Safe today because no writer emits offset suffixes (verified on-disk), but the read side
   has no guard equivalent to the ingester's `verify_utc_roundtrip`.
4. **(pre-existing, informational)** The suite is not root-invocable: 4 `slow`-marked
   `test_regression_backtest.py` tests error on config resolution outside `trading-bot/`. Unrelated
   to this commit.
5. **(unchanged, already in G1)** HYPE absent from archive; coverage stops 2025-12-31.
