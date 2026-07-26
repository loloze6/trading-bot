# `local_data/` — data cache: what is here, what is not, and how to get it

This directory is the flat CSV cache that every `BaseFetcher` subclass reads and writes.
The **loose CSVs at this directory's root are committed** to the repo. **Every
subdirectory is excluded** by `.gitignore` (`trading-bot/local_data/*/`), as is one
oversized root file. This README exists so that exclusion is recoverable rather than
mysterious.

---

## ⛔ DO NOT DOWNLOAD 2026 H1 DATA

**The range `2026-01-01` → `2026-06-30` is a FROZEN, SINGLE-USE holdout.**

Defined at `strategy-research/config/campaign_data_policy.yaml:18` (`holdout_range`),
governed by the rule at that file's lines 8–9 — *"no stage, tool, prescreen, or
diagnostic may read candles inside this range except the (future) holdout_evaluation
stage"* — and by `holdout_failure_is_terminal: true` (`:199`): if a strategy fails on
this range, **no further promotion path exists for it.** The Q1-2026 Kraken tranche was
physically moved out of the in-sample tree and sealed for exactly this reason
(`:151-168`).

Its absence from this repo is **deliberate**, not an oversight.

**Why this matters, concretely.** The whole campaign's claim to have measured anything
honestly rests on one unspent out-of-sample window. That window is worth something only
because *no decision anywhere in the campaign has been influenced by it.* Anyone who
examines, downloads, plots, backtests on, or even eyeballs 2026 H1 data — from **any**
venue, by **any** route (Kraken, Binance, a data vendor, a chart on a website, a
notebook someone shares) — destroys that. Not degrades: destroys. The moment a human or
model has seen how 2026 H1 played out, every subsequent design choice is contaminated by
it, and there is no way to un-see it and no second window in reserve.

The damage is **permanent and undetectable**. Nothing in a later result will look wrong.
The backtest will still print a Sharpe ratio. It will simply no longer mean what it
claims to mean, and no reviewer — including you — will be able to tell from the output
that this happened.

**This is a protocol rule, not a technical control.** Nothing in this repository can
enforce it. `.gitignore` keeps the sealed bytes out of the published tree; it cannot stop
anyone from typing a date range into an exchange API. The rule holds only because the
people working on this campaign choose to hold it. If you need data for development or
debugging, stop at **2025-12-31**.

If you believe you have read 2026 H1 data — even accidentally, even briefly — **say so
immediately**. A disclosed contamination can be reasoned about. An undisclosed one
silently invalidates everything downstream of it.

### ⚠️ This repository shipped 2026 H1 data while saying not to obtain it

Stated plainly, because the section above was written as if the cache stopped at
2025-12-31 and it did not. Measured 2026-07-26 (last-timestamp field only, no value
column read), **seven loose CSVs at this directory's root carry rows inside
`2026-01-01`..`2026-06-30`**:

| File | Last timestamp | Rows in holdout range | Was committed? |
|---|---|---:|---|
| `BTCUSDT_1h.csv` | `2026-07-05 10:00:00` | 4,344 | **yes** |
| `ETHUSDT_1h.csv` | `2026-07-05 10:00:00` | 4,344 | no |
| `BTCUSDT_1d.csv` | `2026-03-19` | 78 | no |
| `ETHUSDT_1d.csv` | `2026-03-19` | 78 | no |
| `fear_greed_daily.csv` | `2026-07-05` | 181 | **yes** |
| `BTCUSDT_funding_8h.csv` | `2026-07-05 08:00:00.001` | 542 | **yes** |
| `ETHUSDT_funding_8h.csv` | `2026-07-05 08:00:00.001` | 542 | no |

**All seven are now excluded from publication** (`.gitignore`, "holdout-carrying cache
files" block); the three that were tracked were removed from the index with
`git rm --cached`. Working copies are untouched — this changes what the repo *publishes*,
not what is on your disk. Registered at
`strategy-research/config/campaign_data_policy.yaml`
(`binance_cache_holdout_contaminated`).

**Repository HISTORY still contains them.** The three tracked files were committed from
`ac27791` (2026-06-12) onward. `git rm --cached` removes a file from the current tree, not
from prior commits, so **a clone of full history is not holdout-clean** — `git show` on any
commit in that range still yields 2026 H1 bars. History rewrite is the operator's separate
decision, filed alongside the same decision for `.env` at `fec0120`. Until then, treat full
history as contaminated and do not check out or diff these paths at older commits.

Two consequences for the rest of this README, noted here rather than by rewriting it:
§3's "committed and published" no longer holds for the seven files above, and §3.5's
funding-carry reproduction now requires re-fetching its two inputs (bounded at
**2025-12-31**) rather than reading them from a clone.

---

## 1. What is NOT in this repo, and why

| Path | Size | Why excluded |
|---|---|---|
| `Kraken_batch/` | **15.3 GB**, 7,582 files (was 32 GB / 25,522 — see §1.1) | Bulk Kraken archive. Far past any practical repo size. |
| `Kraken_funding_rates/` | **436 MB**, 480 CSVs | Bulk Kraken funding export. Size, plus no provenance record (see §2.2). |
| `holdout_sealed/` | **1.9 GB** | **SEALED single-use holdout** — see the section above. Excluded twice over: by `trading-bot/local_data/*/` and by a dedicated `**/holdout_sealed/` rule. |
| `BTCUSDT_1m.csv` | **177,664,416 bytes (≈169 MiB)** | Exceeds **GitHub's 100 MB per-file hard limit**. A push containing it is rejected outright — this is not a soft warning, it blocks the push. **Present on disk — see §2.3, it is not reconstructible from anything else here.** |

`Kraken_batch/` now contains `master_q4/` only — 15.3 GB, 7,582 files: the static year-end
OHLCVT bulk export, at resolutions **1, 60, 240, 720 and 1440 minutes**, plus one
non-conforming `BTCUSD_Daily_OHLC.csv`. This is the directory the ingest tool consumes.

### 1.1 Disk prune, 2026-07-26 (dispatch C1)

15.71 GB was deleted from this directory to recover disk space (free space on `C:` was
down to 0.12 GB). **Nothing deleted was a unique source.** What went, and why:

| Deleted | Size | Why it was safe |
|---|---|---|
| `master_q4/*_5.csv`, `*_15.csv`, `*_30.csv` | 10.37 GB, 4,445 files | Pure downsamples of the retained `_1` files, and **unused** — see the verification below. Re-derivable locally, or re-obtainable from Kraken (§2.1). |
| `Kraken_batch/__MACOSX/` | 2.04 MB, 12,028 files | macOS `._*` resource-fork junk from unzipping on macOS. Not data. (Byte-sum; a `du -sh` reads ~16 MB because 12,028 stubs of ~163 B median each occupy one cluster apiece.) |
| `Kraken_batch/q1_26/` | 5.34 GB, 1,467 files | Superseded **and** holdout-range — see §1.2. |

**`_1` is retained as the reconstruction base.** Every deleted resolution is a strict
aggregation of it, so `_5`/`_15`/`_30` can be rebuilt offline by resampling `_1` — no
download, no network, no holdout exposure. Deletion was scoped to resolutions that were
**both** reconstructible from a retained finer file **and** unused.

**The "unused" claim was verified against real consumers, not asserted.** There are three
live references to `master_q4/`, and each reads a *retained* file:

1. `trading-bot/tools/ingest_kraken_archive.py:281` sets the archive dir, and `:130` builds
   `{pair}_{resolution}.csv` at `RESOLUTION_MINUTES = 60` (`:89`). No caller overrides that
   default — reads `_60`.
2. `trading-bot/tests/test_kraken_archive_ingest.py:32` points at the same directory.
3. `strategy-research/config/campaign_queue.yaml:31` pins `master_q4/*_1440.csv`.

Zero path references to `_5.csv` / `_15.csv` / `_30.csv` exist anywhere in the repo.
`strategy-research/protocols/escalation_tf_15m.json` was checked specifically as the one
plausible consumer: it declares `"timeframe": "15m"` but carries no data path and is
derived from `baseline_v1.json`, so it never sourced `_15.csv`. All three consumer paths
were re-confirmed to resolve after the prune, and the retained set was verified
byte-identical before and after (7,581 files / 16,384,726,678 bytes).

### 1.2 `Kraken_batch/q1_26/` — deleted, was holdout-range

5.34 GB across 1,467 CSVs of Q1-2026 Kraken **Trades** (time-and-sales, not OHLCVT), with
timestamps inside the frozen holdout range, stored in the in-sample tree. Deleted
2026-07-26, unread. It was removed rather than relocated because it was **superseded for
every purpose**: the sealed tranche already holds the same 1,467 pairs as finished OHLCVT
(B1-R: only-in-q1_26 = 0, only-in-sealed = 0, in-both = 1,467), so aggregating it could
only have regenerated data that already exists in final form. Its removal also closes the
contamination vector filed as ledger **G8** — holdout-range bytes sitting beside an active
ingest source — by eliminating the bytes. Re-obtainable from Kraken if ever needed
(§2.1), but **do not re-download it**: it is inside the frozen holdout range (§0).

---

## 2. How to obtain each excluded set

### 2.1 `Kraken_batch/master_q4/` — Kraken bulk historical OHLCVT

**Source (verified, not guessed):** Kraken Support, *"Downloadable historical OHLCVT
(Open, High, Low, Close, Volume, Trades) data"* —
<https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data>
(index page: <https://support.kraken.com/sections/360009899492-csv-data>). Distributed as
ZIP bundles via Google Drive links published in that support article, covering every pair
from the beginning of each market, at intervals 1/5/15/30/60/240/720/1440 minutes, with
quarterly incremental updates. Provenance recorded in
`strategy-research/docs/session_reports/20260721_breadth_download_recon.md:151` and
schema-confirmed in `20260722_kraken_ingest_audit.md:28-53`.

**Format:** headerless, 7 columns —
`unix_timestamp(seconds,UTC), open, high, low, close, volume, trade_count`. Filenames are
`{KRAKEN_TICKER}_{RESOLUTION_MINUTES}.csv`, flat inside `master_q4/`. Kraken uses legacy
base tickers: **`XBT`** for Bitcoin, **`XDG`** for Dogecoin.

**Coverage caveat:** the export is static and terminates **2025-12-31 23:59 UTC**. It is
not a live feed. Kraken's own caveat also applies — *"the OHLCVT data only includes
entries for intervals when trades happened"* — so a gap in a thin pair is a real-market
fact, not a fetch failure.

**Note:** the ~7-month gap between the archive cutoff and the present falls inside the
frozen holdout range. Do not fill it. See §0.

Once downloaded, unzip to `trading-bot/local_data/Kraken_batch/master_q4/` — the ingest
tool hardcodes that path (`trading-bot/tools/ingest_kraken_archive.py:281`).

**What is on disk is a subset.** The upstream ZIPs carry all eight intervals; this cache
retains **1, 60, 240, 720, 1440** only. The `5`, `15` and `30` minute files were pruned
(§1.1). Two ways to get them back, cheapest first:

1. **Resample locally from the retained `_1` files** — no download, no network, and no risk
   of straying past the 2025-12-31 archive cutoff into the frozen holdout. The `_1` files
   are the reconstruction base and are kept precisely for this.
2. **Re-download and re-unzip** the same Kraken bulk ZIPs linked above; they are static and
   still contain every interval. Unzipping on macOS recreates the `__MACOSX/` junk
   directory — delete it, it is not data.

Both routes are bounded by the archive's own **2025-12-31** cutoff, so neither can
introduce holdout-range data. The `q1_26` Trades tranche came from the same support
article's Q1-2026 export; **do not re-obtain it** (§0, §1.2).

### 2.2 `Kraken_funding_rates/exports/` — 480 × `PF_*USD.csv`

**⚠️ NO PROVENANCE RECORD.** This is filed as **ledger item G7**
(`strategy-research/docs/session_reports/20260725_funding_recost_feasibility.md:503-509`).
Stated honestly: there is **no README, no manifest, and no emitting fetcher** anywhere in
`trading-bot/data/fetchers/` that produces these files. `ls -a` on the directory yields
only `__MACOSX` and `exports`. Nobody recorded where or when they came from, so the
account below is *reconstruction*, not documentation.

**What was measured** (per G7): schema is
`timestamp, tradeable, absolute_rate, relative_rate` — **not** the
`timestamp, funding_rate` schema this codebase's loaders require. Cadence is
predominantly **1 hour** (29,279 one-hour gaps vs 1,145 four-hour, measured on
`PF_XBTUSD`), not the 8-hour Binance convention. Coverage begins **2022-03-22**. Naming
is `PF_{BASE}USD.csv` — Kraken Futures perpetual symbols.

**Most likely source**, consistent with those properties: the Kraken Support **"Export
funding rates"** UI action —
<https://support.kraken.com/articles/export-historical-funding-rates> — which delivers a
ZIP of per-pair CSVs "since inception". Whether it requires an authenticated Kraken
session was never confirmed
(`20260721_breadth_download_recon.md:156`, flagged open at `:160`). **Treat this
attribution as unverified until someone re-runs the export and diffs the output against
what is on disk.**

**Consequence:** this archive is currently **structurally unloadable** — wrong filename
convention, wrong schema, wrong cadence, and its 2022-03-22 start cannot reach the
2019-12 start of the funding-analysis window. It is not a drop-in substitute for the
Binance `*_funding_8h.csv` files that *are* committed here.

### 2.3 `BTCUSDT_1m.csv` — regenerate, do not download

**Retained on disk; excluded from the repo only by size.** It was a candidate in the
2026-07-26 prune (§1.1) and was withdrawn before deletion, for a reason worth stating
explicitly because §1.1 emphasises `_1` as "the reconstruction base": **that base is
Kraken, and this file is Binance.** `master_q4/*_1.csv` cannot regenerate it. The two are
different venues with different prints, and substituting one for the other would
reintroduce exactly the fee/venue mismatch Phase 1 closed. Deleting this file would
therefore have cost an API re-fetch, not a local resample — so it stays.

Produced by `CcxtFetcher` against Binance at 60-second resolution. `exchange="binance"`
takes the **un-prefixed** cache key (`ccxt_fetcher.py:120-121`), so the file lands back at
exactly this name:

```python
# run from trading-bot/
from data.fetchers.ccxt_fetcher import CcxtFetcher

CcxtFetcher(
    start_date="2018-01-01",
    end_date="2025-12-31",          # STOP HERE — 2026 H1 is the frozen holdout
    symbols=["BTCUSDT"],
    candle_interval_seconds=60,
    exchange="binance",
    localStorage=True,
    data_dir="local_data",
).get_data()
```

`BaseFetcher` gap-fills incrementally, so a partial file is topped up rather than
refetched. Expect a long run — this is ~178 MB of 1-minute bars over paginated
1000-row calls.

`data.binance.vision` (Binance's free public bulk archive, no registration) is the faster
route for the same bytes. It is acceptable **for BTCUSDT_1m specifically**, since that
series is already Binance-sourced. It is **not** acceptable as a substitute for
Kraken price data — mixing venues reintroduces the fee/venue mismatch Phase 1 closed
(`20260721_breadth_download_recon.md:162`).

---

## 3. What IS in this repo

All files below are loose CSVs at this directory's root, committed and published.

### 3.1 Binance spot OHLCV — `CcxtFetcher`

`AVAXUSDT_1h.csv`, `AVAXUSDT_4h.csv`, `BTCUSDT_1d.csv`, `BTCUSDT_1h.csv`,
`ETHUSDT_1d.csv`, `ETHUSDT_1h.csv`, `SOLUSDT_1h.csv`, `SOLUSDT_4h.csv`

Produced by `trading-bot/data/fetchers/ccxt_fetcher.py:36` with `exchange="binance"`
(default, `:54`). Cache key is `{prefix}{symbol}_{ccxt_timeframe}` where the prefix is
**empty for Binance** and `{exchange_id}_` otherwise (`ccxt_fetcher.py:101-121`) — that
backward-compatibility carve-out is why these are un-prefixed while the Kraken files
below are not.

### 3.2 Kraken spot OHLCV — `ingest_kraken_archive.py`

19 files: `kraken_{AAVE,ADA,AVAX,BTC,DOGE,ETH,INJ,LINK,LTC,NEAR,ONDO,SOL,SUI,TAO,TRX,UNI,XMR,XRP,ZEC}USD_1h.csv`

**Not** live-fetched. Converted from `Kraken_batch/master_q4/` (§2.1) by
`trading-bot/tools/ingest_kraken_archive.py` — see `:281` (archive path), `:240-248`
(per-asset ingest), `:110-130` (source-ticker mapping). The tool remaps Kraken's legacy
source tickers to market-standard store symbols (`XBT`→`BTC`, `XDG`→`DOGE`,
`ingest_kraken_archive.py:20`) and writes into the `kraken_`-prefixed `CcxtFetcher` cache
slot, so the fetcher layer reads them transparently. Coverage inherits the archive's
2025-12-31 cutoff.

### 3.3 Funding rates — `FundingRateFetcher` (**Binance convention**)

`AVAXUSDT_funding_8h.csv`, `BTCUSDT_funding_8h.csv`, `ETHUSDT_funding_8h.csv`,
`SOLUSDT_funding_8h.csv`

Produced by `trading-bot/data/fetchers/funding_rate_fetcher.py:51` with
`exchange_id="binance"` (default, `:69`; class docstring `:57`). Cache key is
`{symbol}_funding_8h` (`:106-108`) — note this key is **not** exchange-qualified, unlike
`CcxtFetcher`'s, so a second-venue funding fetch would silently overwrite these.

These are **Binance perpetual-futures funding**: three settlements per day at an 8-hour
cadence. Do not conflate them with the Kraken `PF_*USD.csv` archive in §2.2, which is a
different venue, a different schema, and a ~1-hour cadence. Inception dates:
BTCUSDT 2019-09-10, ETHUSDT 2019-11-27 (`campaign_data_policy.yaml:26-27`).

### 3.4 Sentiment — `FearGreedFetcher`

`fear_greed_daily.csv` — produced by `trading-bot/data/fetchers/fear_greed_fetcher.py:54`,
cache key `fear_greed_daily` (`:91-93`). Source is alternative.me's Fear & Greed index,
daily, history starts 2018-02-01 (`campaign_data_policy.yaml:25`).

### 3.5 Reproducing the funding-carry analysis

`strategy-research/docs/session_reports/20260725_funding_carry_magnitude.md` is fully
reproducible from what is committed here — it needs **no excluded data**. It consumes
exactly two files, both present:

- `trading-bot/local_data/BTCUSDT_funding_8h.csv`
- `trading-bot/local_data/ETHUSDT_funding_8h.csv`

Run `strategy-research/tools/measure_funding_carry.py` (input paths declared at `:4-5`,
resolved at `:29-42`, columns used: `timestamp`, `funding_rate`). The daily-aggregation
semantics it mirrors live in `trading-bot/data/feed_registry.py`
(`build_daily_funding_series`). The report's own window is bounded to exclude the frozen
holdout range and the sealed Kraken Q1 tranche
(`20260725_funding_carry_magnitude.md:60`, `:240`).

---

## 4. `.gitignore` policy for this directory

The rule is **deny-by-default on subdirectories**:

```
trading-bot/local_data/*/          # every subdirectory, present and future
**/holdout_sealed/                 # belt-and-braces on the sealed holdout
trading-bot/local_data/BTCUSDT_1m.csv
```

This is deliberately *not* an enumeration of the three known bulk directories. A new bulk
directory dropped in here later is excluded automatically, without anyone remembering to
update a list. If you add a small file at this directory's **root**, it will be published
— check its size first.
