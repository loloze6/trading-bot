# Phase 2 Track A Recon: Breadth Download Plan (price + funding, ~20 liquid Kraken pairs)

**Model:** Claude Sonnet 4.6 (recon, read-only)
**Date:** 2026-07-21
**Precondition manifest:** HEAD = `ad11fbd` at start, `git status --porcelain` empty. Both confirmed before any read.
**Status:** written plan only. No data downloaded, no code written, `feed_wishlist.yaml`/`campaign_queue.yaml`/any brief untouched.

---

## Step 1 — `feed_wishlist.yaml`: schema, and is it mechanically gated?

### Schema (as it exists today)

`strategy-research/feed_wishlist.yaml` — single top-level `wishlist:` list. Per-entry fields (from the file's own header comment + the one real entry):

```yaml
version: "1.0"
created_at: <ISO date>
wishlist:
  - feed_name: string                       # canonical name, matches available_feeds.yaml's unavailable list
    evidence_type: string                   # the evidence_type enum value this feed would satisfy
    hypotheses_blocked: [string, ...]        # hypothesis_ids/descriptions blocked without this feed
    priority_rationale: string               # why the feed matters
    estimated_hypotheses_unblocked: int
    created_at: ISO date
    last_updated: ISO date
    trigger_condition:                       # OPTIONAL — see below
      predicate:
        source: kb_finding | campaign_queue
        all_of: [{field, op, value}, ...]
      status / last_evaluated_at / last_evaluated_against / kb_state_hash / evaluation_note   # write-only, evaluator-populated
```

Currently there is exactly **one** entry (`liquidation_data`), and it has **no `trigger_condition` block at all** — only the prose fields (`feed_name`, `evidence_type`, `hypotheses_blocked`, `priority_rationale`, `estimated_hypotheses_unblocked`, `created_at`, `last_updated`).

### Is it mechanically checked, or documentation-only?

**Both — it depends on the entry.** `strategy-research/workflow/run_campaign.py` contains a real, working evaluator for this file:

- `_wishlist_family_names()` (L478-492) — collects every `feed_name` (and `detector_wishlist.yaml`'s `family` names) into one list.
- `_find_wishlist_entry()` (L526-541) — looks up one family's own entry.
- `evaluate_wishlist_predicate()` (L597-645) — reads that entry's `trigger_condition.predicate`, evaluates it against either `campaign_knowledge_base.yaml`'s findings or `config/campaign_queue.yaml`'s queue (per `predicate.source`), and returns `triggered` / `not_triggered` / `data_gap`.
- `evaluate_and_persist_wishlist_predicate()` (L651-726) — the **sole** function permitted to write `status`/`last_evaluated_*`/`kb_state_hash` back into the wishlist file (this authority is explicit in its own docstring, added 2026-07-10 specifically because an earlier hand-authored `status` field had gone stale with no code path ever having written it).
- `_check_wishlist_trigger()` (L729-757) — a **hard pause**: if `campaign_review`'s recommendation is `reframe` or `escalate_component` and its `next_research_question`/`recommendation_rationale` text mentions a wishlist family name, the campaign runner stops rather than letting a recommendation silently consume an unvetted wishlist family. This is what closed the run_045/run_046 failure mode referenced in the docstring (a recommendation drew on a wishlist family without anyone — human or code — checking its `trigger_condition`).

So the mechanism is real and load-bearing, not decorative. **But** it only activates for entries that have populated a `trigger_condition.predicate`. Calling `evaluate_wishlist_predicate("liquidation_data")` today would hit line 623-627 and return:

> `"missing_field"` — *"family 'liquidation_data' has no trigger_condition.predicate (still prose-only -- rewrite it before this can auto-evaluate)"*

i.e. the file's one real entry is currently **prose-only** by the evaluator's own admission — it exists as a human-readable backlog item, and would only become mechanically gate-worthy if someone added a `trigger_condition.predicate` to it.

### The dispatch's example — does `XS_momentum`'s `blocked_on_P2` actually check against `feed_wishlist.yaml`?

**No — checked directly, and this is not the case.** `config/campaign_queue.yaml` L172-186:

```yaml
- id: XS_momentum
  brief_path: briefs/research_brief_XS_momentum.md
  status: blocked_on_P2
  priority: 2
  source: agent
  notes: 'Cross-sectional momentum needs a real cross-section of low-correlation instruments;
    the campaign currently covers only BTCUSDT/ETHUSDT (rho=0.82, n_eff_symbols≈1.10
    per config/campaign_config.yaml). P2 = instrument-universe expansion (fetch-verify
    OHLCV for a broader coin_universe.yaml set, update campaign_data_policy.yaml,
    re-measure correlations). See the brief''s own "What P2 must deliver" section
    for the unblock checklist. Do not flip to ready until that checklist is done.'
  run_ids: []
  outcome: null
```

`status: blocked_on_P2` is a **plain, hand-authored string** on the queue entry. It is not a `trigger_condition`, it has no `predicate`, and it is not read by `evaluate_wishlist_predicate()` / `_wishlist_family_names()` (those only look at `detector_wishlist.yaml` candidates and `feed_wishlist.yaml` wishlist entries — `XS_momentum` is neither; it's a `campaign_queue.yaml` entry, a different file, with no code path connecting the two). Its "unblock checklist" is prose in the brief, not a machine predicate. **The dispatch's parenthetical framing is inaccurate as stated** — `blocked_on_P2` is unrelated to the `feed_wishlist.yaml` mechanism; it references a data-breadth task (P2) directly, with no wishlist gate in between.

---

## Step 2 — `DataManager`'s existing cache/consistency layer

Full file read: `trading-bot/data/data_manager.py` (988 lines) plus its two fetcher dependencies, `trading-bot/data/fetchers/base_fetcher.py` and `trading-bot/data/fetchers/ccxt_fetcher.py`.

### (a) Local storage/cache mechanism

- **Where:** `trading-bot/local_data/` (`data_manager.fetch_historical_data()`, L761-763: `data_storage_dir = os.path.join(project_folder, "local_data")`, `project_folder` = `trading-bot/`).
- **Format:** flat CSV, one file per (symbol, timeframe) — or per aux-feed key.
- **Keying:** `BaseFetcher._csv_path()` (`base_fetcher.py` L209-211) → `{data_dir}/{cache_key(symbol)}.csv`. `CcxtFetcher.cache_key()` (`ccxt_fetcher.py` L101-105) → `f"{symbol}_{self.ccxt_timeframe}"`, e.g. `BTCUSDT_1h.csv`. Aux feeds key their own cache files the same way through their own `cache_key()` overrides (e.g. `BTCUSDT_funding_8h.csv`, `fear_greed_daily.csv` — confirmed present in `local_data/`, see below).
- **Date-range handling:** not baked into the filename — one file accumulates the symbol's *entire* fetched history; `BaseFetcher._load_all()` (L164-203) trims to the caller's requested `[start_date, end_date]` window in memory after loading/merging, it does not split files by range.
- **Fetch entry point actually used by the bot:** `DataManager.fetch_historical_data(symbol, start_date, end_date)` (L746-790) constructs a `CcxtFetcher(..., exchange="binance", localStorage=True, data_dir=local_data)` — **`exchange="binance"` is hardcoded** at this call site (not parameterized), even though `CcxtFetcher.__init__` itself accepts any CCXT exchange id string.

### (b) Existing consistency checks — quoted, not inferred

Three real, already-working checks live in `BaseFetcher` (inherited by `CcxtFetcher` and any future feed fetcher for free):

1. **Gap detection** — `_identify_missing_periods()` (`base_fetcher.py` L253-315). Three gap types: before the earliest stored row, after the latest stored row, and internal gaps `> expected_gap_tolerance × interval_seconds` (default tolerance 1.5×):
   ```python
   for i in range(1, len(timestamps)):
       gap = timestamps[i] - timestamps[i - 1]
       if gap > expected * self.expected_gap_tolerance:
           gs = pd.Timestamp(timestamps[i - 1] + expected).to_pydatetime().replace(tzinfo=None)
           ge = pd.Timestamp(timestamps[i] - np.timedelta64(1, "ms")).to_pydatetime().replace(tzinfo=None)
           ...
   ```
   This drives **incremental fetch** — `_load_all()` only re-fetches the missing periods, not the whole range, on repeat calls.

2. **Post-load continuity report** — `validate_data_continuity()` (`base_fetcher.py` L138-158), a read-only re-scan of the same gap logic over the final cached data, called from `DataManager.fetch_historical_data()` (L775) and logged (`logger.warning` if gaps found) — this is diagnostic, not a hard fail.

3. **Deduplication** — `_merge_and_store()` (`base_fetcher.py` L232-247):
   ```python
   combined = (
       pd.concat(pieces, ignore_index=True)
       .drop_duplicates(subset=["timestamp"])
       .sort_values("timestamp")
       .reset_index(drop=True)
   )
   ```

**No timestamp/timezone validation exists at this layer.** `_load_local()` does `df["timestamp"] = pd.to_datetime(df["timestamp"])` (L226) with no explicit UTC handling, and `CcxtFetcher._fetch_remote()` does `pd.to_datetime(df["timestamp"], unit="ms")` (L172, epoch-ms → naive UTC by pandas convention) — there is no assertion, no round-trip check, nothing that would catch a fetcher subclass that returned local-time-interpreted timestamps. This matters directly for step 4 below.

### (c) What's actually in the cache right now

`trading-bot/local_data/` (13 CSVs, all Binance-sourced since `exchange="binance"` is hardcoded):

| File | Rows | First | Last |
|---|---|---|---|
| BTCUSDT_1d.csv | 3,137 | 2017-08-17 | 2026-03-19 |
| BTCUSDT_1h.csv | 74,457 | 2018-01-01 | 2026-07-05 10:00 |
| BTCUSDT_1m.csv | 1,577,500 | 2022-03-31 22:00 | 2025-04-01 04:59 |
| BTCUSDT_funding_8h.csv | 7,468 | 2019-09-10 08:00 | 2026-07-05 08:00 |
| ETHUSDT_1d.csv | 3,137 | 2017-08-17 | 2026-03-19 |
| ETHUSDT_1h.csv | 74,457 | 2018-01-01 | 2026-07-05 10:00 |
| ETHUSDT_funding_8h.csv | 7,234 | 2019-11-27 08:00 | 2026-07-05 08:00 |
| AVAXUSDT_1h.csv | 8,987 | 2024-01-01 | 2025-01-09 10:00 |
| AVAXUSDT_4h.csv | 2,998 | 2023-11-27 | 2025-04-09 12:00 |
| AVAXUSDT_funding_8h.csv | 2,104 | 2023-11-27 | 2025-10-28 |
| SOLUSDT_1h.csv | 8,987 | 2024-01-01 | 2025-01-09 10:00 |
| SOLUSDT_4h.csv | 2,998 | 2023-11-27 | 2025-04-09 12:00 |
| SOLUSDT_funding_8h.csv | 2,104 | 2023-11-27 | 2025-10-28 |
| fear_greed_daily.csv | 3,073 | 2018-02-01 | 2026-07-05 |

Note (not previously surfaced, worth flagging): the cache already holds AVAX and SOL alongside BTC/ETH — `XS_momentum`'s queue note ("the campaign currently covers only BTCUSDT/ETHUSDT") describes what the *campaign registers/uses*, not what's on disk. The extra breadth already cached is short-range (~14 months) and Binance-sourced, i.e. it doesn't resolve P2 on its own (wrong venue for the now-decided Kraken cost model, and short history), but it means a 4-coin pilot really could start before the full 20-pair pull lands, as ROADMAP.md 2.2 already anticipates.

### Verdict: reuse existing mechanism, with one small, justified extension

**Reuse, not new plumbing**, for the storage/gap/dedup layer — `BaseFetcher`/`CcxtFetcher` already do exactly what a 20-pair breadth pull needs: per-symbol CSV cache, incremental gap-fill, dedup, continuity report. The **one concrete gap** is that `exchange="binance"` is hardcoded at the single call site in `DataManager.fetch_historical_data()` (L765-771) — pulling from Kraken requires either parameterizing that call with `exchange="kraken"` or calling `CcxtFetcher` directly with `exchange="kraken"` from the breadth-download script (both are within `CcxtFetcher`'s existing constructor contract; no class needs to change). This is a minimal, additive parameter change, not new infrastructure.

---

## Step 3 — Kraken's public historical-data surface (verified live, 2026-07-21)

### (a) OHLCV price history

- **REST endpoint:** `GET /public/OHLC` (`pair`, `interval` in minutes: 1/5/15/30/60/240/1440/10080/21600, optional `since`). **Hard limit: returns only the 720 most recent candles; "older data cannot be retrieved, regardless of the value of `since`."** [^1] This endpoint alone **cannot** serve a multi-year backfill for 20 pairs — it's only useful for incremental top-up once a base history exists.
- **Bulk historical download (the actual backfill source):** Kraken publishes a "Downloadable historical OHLCVT" dataset — ZIP/CSV files per pair, covering **every pair's full history "from the beginning of each market up to the present,"** at the same interval set (1/5/15/30/60/240/720/1440 min), distributed via Google Drive links from the support article, with quarterly incremental updates for those who already have the base file. Caveat quoted directly: *"the OHLCVT data only includes entries for intervals when trades happened, so any missing candlesticks indicate that no trades occurred during those intervals"* — i.e. sparse-trading gaps are a legitimate real-market signal here, not a fetch failure, and must not be flagged the same way as a fetch gap. [^2]

### (b) Funding-rate history (Kraken Futures)

- **REST endpoint:** `GET /historical-funding-rates` (Futures API), required `symbol` param in Futures format (e.g. `PF_BTCUSD`). Returns a `rates` array (ascending by timestamp) of `{fundingRate, relativeFundingRate, timestamp (ISO 8601)}`. **No documented pagination or date-range parameters** — the docs page doesn't state retention depth or a `from`/`to` filter. [^3]
- **Bulk export (UI-based):** Kraken Support provides an **"Export funding rates"** button that downloads a CSV bundle "containing funding rate data for each trading pair **since inception**" — i.e. full history per pair, no filtering, delivered as a ZIP of CSVs. This is a UI action inside the Support Center; whether it requires an authenticated Kraken account session was **not confirmed** in this pass — flagged for implementation-time verification, same discipline as the venue survey's own open items. [^4]

### Gap assessment and fallback

**No blocking gap for a 20-pair, multi-year pull** — Kraken's own bulk OHLCVT CSV download and the funding "since inception" export both cover the full history needed; the 720-candle *REST* cap only limits the live/incremental-poll path, which the existing `BaseFetcher` gap-fill logic (step 2b) is already built to use correctly (small top-up fetches, not full backfills). Two open items to resolve before implementation, not resolved here: (i) whether the funding CSV export needs an authenticated session, (ii) exact retention depth of the `/historical-funding-rates` REST endpoint (undocumented — could be shallower than "since inception"; the bulk export is the safer default source for a multi-year pull specifically because it states its depth explicitly and the REST endpoint doesn't).

**Fallback source considered:** `cryptodatadownload.com`'s Kraken dataset was checked live and is **currently unavailable** ("If you need this data, please reach out to us and we will happily refer you to a 3rd party provider") [^5] — not usable as a fallback right now. Given Kraken's own bulk download already covers the need, the one fallback worth naming is **Binance's public bulk archive**, `data.binance.vision` [^6] — free, no registration, long history, and it's the same source the repo's existing Binance-sourced `local_data` cache already draws its live data from via `ccxt`. It should be used **only as a cross-check for data-quality sanity** (e.g. comparing candle counts/gap patterns on a shared pair like BTC), **not as a substitute price series** for the Kraken-costed backtest — mixing venues would reintroduce exactly the venue/fee mismatch Phase 1 just closed.

---

## Step 4 — Timezone fix, commit `2529f5b`

```
commit 2529f5b596eab206c8ed5afec830f2fefbec69b4
Engine fix: CandleBuilder._align() used naive local-timezone epoch round-trip
instead of UTC — silent zero-forecast at 1d (run_059); adds first 1d
regression coverage for FundingRateMeanReversionComponent
```

Diff, `trading-bot/data/data_manager.py`, inside `CandleBuilder._align()`:

```diff
-        ts = int(timestamp.timestamp())
+        ts = int(timestamp.replace(tzinfo=datetime.timezone.utc).timestamp())
+        aligned_ts = (ts // self.interval_seconds) * self.interval_seconds
         return datetime.datetime.fromtimestamp(
-            (ts // self.interval_seconds) * self.interval_seconds
-        )
+            aligned_ts, tz=datetime.timezone.utc
+        ).replace(tzinfo=None)
```

**The bug:** all price/candle timestamps in this codebase are naive datetimes meant to represent UTC instants. Naive `datetime.timestamp()` / `datetime.fromtimestamp()` silently interpret and re-emit through the **local system timezone**. For `interval_seconds` that are an exact multiple of the local UTC offset (e.g. 3600s/1h — any whole-hour offset cancels through the floor division) this is a no-op and invisible. For `interval_seconds` that are **not** (e.g. 86400s/1d, on a non-UTC machine), it silently shifts every aligned candle boundary to a fixed non-zero hour, every day. Confirmed root cause: `run_059`'s all-bars-zero forecast at 1d — `FundingRateMeanReversionComponent`'s settlement-boundary check (`hour % 8 == 0`) never matched because daily candles were landing on `hour=01` (or `02` under DST), never `hour=00`.

**The established pattern:** an explicit UTC round-trip — `timestamp.replace(tzinfo=timezone.utc).timestamp()` in, `datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)` out — for any code that does interval-boundary arithmetic on a naive UTC-instant datetime.

**Does that check already live inside `DataManager` (per step 2), or elsewhere?** — **Elsewhere, precisely.** It lives in `CandleBuilder._align()` only — the in-memory candle-boundary aggregation logic shared by live tick ingestion and backtest replay. It is **not** inherited by, or present in, `BaseFetcher`/`CcxtFetcher`'s raw fetch/cache layer (`_load_local()` does a bare `pd.to_datetime(df["timestamp"])`, `_fetch_remote()` a bare `pd.to_datetime(df["timestamp"], unit="ms")` — neither does an explicit UTC round-trip). This is a live implication for Phase 2: **any new code the breadth-download plan adds that does its own interval-boundary math** (e.g. verifying Kraken's 1-hour EEA funding settlement boundaries, or resampling raw funding rows onto candle boundaries) **must apply the same explicit-UTC pattern itself** — it will not get it for free from `DataManager`/`BaseFetcher`, and Kraken's funding-settlement-boundary check is structurally the same shape of bug that bit `FUNDING_MR_DAILY_RETEST` (an hour-modulo check against a candle boundary).

---

## Step 5 — Proposed ~20-pair list

**Criterion (stated, checkable):** 24h quoted USD trading volume on Kraken, ranked descending, one pair per distinct base asset (picking whichever of that asset's USD/USDT quote pair has the higher volume), excluding: stablecoin base assets (USDT, USDC), fiat-vs-fiat and stablecoin-vs-stablecoin pairs, and tokenized-equity products (`SPYX` — an S&P 500 tracker token, not a crypto asset). Source: CoinGecko's public exchange-tickers API, `https://api.coingecko.com/api/v3/exchanges/kraken/tickers`, snapshot fetched 2026-07-21. [^7] This is a **single-snapshot 24h ranking** — noisy day to day; recommend the implementation dispatch re-derive it from a 30-day average (via Kraken's own `Ticker`/`AssetPairs` endpoints, first-party) rather than reusing this exact snapshot verbatim.

| Rank | Symbol (Kraken CCXT pair) | 24h USD volume |
|---|---|---|
| 1 | BTC/USD (`XBT/USD`) | $118,825,322 |
| 2 | ETH/USD | $42,820,920 |
| 3 | XRP/USD | $14,725,338 |
| 4 | SOL/USD | $12,611,741 |
| 5 | ADA/USD | $10,040,431 |
| 6 | SUI/USD | $8,097,433 |
| 7 | ZEC/USD | $7,294,107 |
| 8 | DOGE/USD (`XDG/USD`) | $6,261,005 |
| 9 | HYPE/USD | $4,126,650 |
| 10 | XMR/USDT | $3,843,424 |
| 11 | LTC/USD | $2,745,914 |
| 12 | ONDO/USD | $2,366,599 |
| 13 | NEAR/USD | $2,308,801 |
| 14 | LINK/USD | $2,153,627 |
| 15 | TAO/USD | $1,896,283 |
| 16 | AVAX/USD | $1,403,604 |
| 17 | TRX/USD | $1,207,525 |
| 18 | AAVE/USD | $990,665 |
| 19 | INJ/USD | $964,786 |
| 20 | UNI/USD | $824,586 |

Note on naming convention: Kraken's liquid pairs are dominantly **USD**-quoted, not USDT-quoted, unlike the existing Binance-sourced `local_data` cache (`BTCUSDT`, `ETHUSDT`, ...). A Kraken pull would produce `cache_key()`s like `BTC_USD_1h.csv` (CCXT-normalized `BTC/USD` → whatever `cache_key()` derives), which is a genuine naming-convention divergence from the current cache, not just a cosmetic one — worth deciding explicitly in the implementation dispatch (e.g. keep Binance-style `BTCUSD` compact symbols, or adopt CCXT's `BASE/QUOTE`) rather than letting it fall out accidentally.

---

## Step 6 — Storage format and integrity-check spec

**Reuses `DataManager`'s existing cache mechanism** (per step 2's finding) — no new storage layer. Concretely:

- **Location:** `trading-bot/local_data/` (unchanged).
- **Format:** flat CSV, unchanged (`BaseFetcher._merge_and_store()`).
- **Keying:** `{symbol}_{timeframe}.csv` via `CcxtFetcher.cache_key()`, and a parallel `{symbol}_funding_{interval}.csv` convention for the new Kraken Futures funding fetcher (mirroring the existing `BTCUSDT_funding_8h.csv` pattern) — a new `KrakenFundingFetcher(BaseFetcher)` subclass is the natural fit for the existing `_fetch_remote()`/`cache_key()` contract; not a new mechanism, an application of the existing one (same shape as `FundingRateFetcher` already used for Binance funding).
- **Extension required, and why it's justified:** `DataManager.fetch_historical_data()`'s hardcoded `exchange="binance"` (L765-771) needs to become a parameter so the same call can target `exchange="kraken"`. This is the one deliberate, minimal change — everything else in `CcxtFetcher`/`BaseFetcher` already accepts it (the constructor already takes `exchange` as an argument; only this one call site pins it).

**Integrity-check spec:**

| Check | Reused from existing mechanism? | Notes |
|---|---|---|
| Gap detection | **Reused** — `BaseFetcher._identify_missing_periods()` / `validate_data_continuity()` | Must set `expected_gap_tolerance` appropriately per feed (price data: default 1.5×; funding at Kraken's EEA 1-hour interval: tolerance should be tuned against real observed cadence, not assumed 8h like the existing Binance funding fetcher — confirm actual interval empirically before reusing the default) |
| Duplicate-row detection | **Reused** — `BaseFetcher._merge_and_store()`'s `drop_duplicates(subset=["timestamp"])` | No change needed |
| Timestamp/timezone consistency | **New — does not exist in the reused layer today** (per step 4's finding) | Must add an explicit UTC-round-trip assertion at ingestion for the new Kraken fetcher(s), following `CandleBuilder._align()`'s established pattern — this is not inherited for free and is exactly the class of bug that caused `run_059` |
| Provenance metadata (source, pull date, date range) | **New** | `BaseFetcher`/`CcxtFetcher` currently store no metadata alongside the CSV — no `source`/`fetched_at`/`exchange` columns or sidecar file exists anywhere in the reused mechanism. A minimal addition (e.g. a sidecar `{cache_key}.meta.json` with `{exchange, fetched_at, requested_range}`, written by `_merge_and_store()`) is needed; this is new but small, and consistent with "reuse the mechanism, extend where a real gap exists" rather than inventing a parallel store |
| Sparse-trading vs. missing-data distinction | **New** | Kraken's own OHLCVT caveat (step 3a) — a "gap" in a low-volume Kraken altcoin pair may mean no trades occurred, not a fetch failure. The existing gap-detection code has no way to distinguish these; worth a note (not necessarily a code change) in the integrity spec so a human reviewing gap reports doesn't treat every flagged gap as a fetch defect |

---

## Bounded report-back

1. **Feed wishlist gate:** mechanically real (`run_campaign.py`'s `evaluate_wishlist_predicate`/`_check_wishlist_trigger`), but the file's one entry (`liquidation_data`) has no `trigger_condition` and evaluates to `missing_field`/"still prose-only" today — it is not currently an active gate. `XS_momentum`'s `blocked_on_P2` is unrelated to this mechanism (plain queue-status string, not a wishlist predicate) — the dispatch's parenthetical was incorrect and I'm flagging it as such rather than assuming it.
2. **Cache mechanism:** reuse, not new plumbing. `BaseFetcher`/`CcxtFetcher` already provide per-symbol CSV cache + incremental gap-fill + dedup; the only change needed is parameterizing the hardcoded `exchange="binance"` in `DataManager.fetch_historical_data()`.
3. **Pair list:** 20 pairs above (BTC, ETH, XRP, SOL, ADA, SUI, ZEC, DOGE, HYPE, XMR, LTC, ONDO, NEAR, LINK, TAO, AVAX, TRX, AAVE, INJ, UNI), criterion = 24h Kraken USD volume via CoinGecko's exchange-tickers API, single-snapshot — recommend re-deriving from a 30-day average before implementation.
4. **Data sources:** Kraken's REST `/public/OHLC` is capped at 720 candles (unusable alone for backfill); the bulk "Downloadable historical OHLCVT" CSV/ZIP (full history per pair) is the real backfill source. Funding: REST `/historical-funding-rates` (undocumented depth/pagination) or the UI "Export funding rates" CSV bundle ("since inception," auth requirement unconfirmed). No blocking gap found; `data.binance.vision` proposed as a cross-check-only fallback (cryptodatadownload.com's Kraken data is currently unavailable, checked live).
5. **Timezone-check requirement (from `2529f5b`):** explicit UTC round-trip (`replace(tzinfo=utc).timestamp()` → `fromtimestamp(ts, tz=utc).replace(tzinfo=None)`) for any interval-boundary arithmetic on naive datetimes. Confirmed this lives only in `CandleBuilder._align()`, not in `BaseFetcher`/`DataManager`'s cache layer — the new Kraken funding fetcher's own settlement-boundary logic must implement this pattern itself; it will not inherit it.

[^1]: Kraken Developers, Get OHLC Data — https://docs.kraken.com/api/docs/rest-api/get-ohlc-data (accessed 2026-07-21)
[^2]: Kraken Support, Downloadable historical OHLCVT data — https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data (accessed 2026-07-21)
[^3]: Kraken Developers, Historical funding rates — https://docs.kraken.com/api/docs/futures-api/trading/historical-funding-rates (accessed 2026-07-21)
[^4]: Kraken Support, Export historical funding rates — https://support.kraken.com/articles/export-historical-funding-rates (accessed 2026-07-21)
[^5]: CryptoDataDownload, Kraken dataset page (currently unavailable) — https://www.cryptodatadownload.com/data/kraken/ (accessed 2026-07-21)
[^6]: Binance Data Collection (public bulk archive) — https://data.binance.vision/ (accessed 2026-07-21)
[^7]: CoinGecko public API, Kraken exchange tickers — https://api.coingecko.com/api/v3/exchanges/kraken/tickers (accessed 2026-07-21)

---

## Addendum (2026-07-21, same-day correction to Step 3a's scope)

Step 3a, as originally committed, verified Kraken's **spot** `/public/OHLC` endpoint only (720-candle hard cap, "older data cannot be retrieved, regardless of the value of `since`") and recommended the bulk OHLCVT CSV download as the backfill path on that basis. It did not check whether **Kraken Futures** (the perpetual-futures product itself) has a separate price-candle endpoint with different behavior. It does, and the behavior looks materially different — this addendum records that finding without altering the original step 3 text above.

**Kraken Futures candles endpoint:**

```
GET https://futures.kraken.com/api/charts/v1/{tick_type}/{symbol}/{resolution}
```

e.g. `.../trade/PI_XBTUSD/1D`. Parameters: `tick_type` (`mark` / `spot` / `trade`), `symbol` (Futures-format, e.g. `PI_XBTUSD`), `resolution` (`1m, 5m, 15m, 1h, 4h, 12h, 1d, 1w`), and — unlike the spot endpoint — explicit `from`/`to` (epoch seconds). The response includes a `more_candles` boolean.

**Why this looks different from spot, not just a variant of the same cap:** the spot endpoint has only a `since` parameter and documents outright that older data is unreachable through it, full stop — the 720-candle window is a hard wall, which is exactly why step 3a routed to the bulk CSV download. The Futures endpoint additionally exposes a `to` parameter and a `more_candles` flag — the shape of a real pagination mechanism (walk `to` backward, or `from` forward, across multiple calls) rather than a hard wall. If that reading is correct, Kraken Futures price history could be backfilled directly through the REST API, with no bulk-CSV workaround needed at all — a different acquisition path than spot.

**Confidence caveat — explicitly not fully confirmed:** three attempts to fetch the primary documentation pages for this endpoint (`docs.kraken.com/api/docs/futures-api/charts/candles`, `.../charts/charts`, `.../trading/historical-data`) all returned HTTP 404 to a direct (non-JS) fetch — likely a client-rendered docs site that doesn't serve static HTML to a plain fetcher, inconsistent with two *other* Kraken docs pages ([^1], [^3] above) that did resolve. The endpoint shape and parameters above were corroborated instead via a third-party API wrapper's documentation, `python-kraken-sdk`[^8], and cross-referenced against general web search results describing the same shape[^9] — **not** the primary source. Per this report's own citation discipline (flag, don't assert, when a claim can't be directly confirmed): treat "Futures candles are genuinely paginable back through full history" as **plausible, not confirmed**. It needs a direct primary-source check (or a live test call) before being relied on for implementation.

**Practical implication — an open item, not resolved by this recon:** which price series each of the 20 pairs should actually use — Kraken **spot** or Kraken **Futures** (perp) — is not decided here. For any pair sourced from Futures (plausible for the funding-based signals specifically, since a funding strategy arguably wants the perp's own price, not spot), the original step 3's bulk-CSV recommendation does not apply — the acquisition path may be the paginated Futures REST endpoint instead, pending the confirmation above. Whoever writes the implementation dispatch needs to (1) decide spot-vs-Futures price sourcing per pair/signal, and (2) directly confirm the Futures candles pagination behavior (primary docs or a live test call) before committing to either acquisition path for those pairs.

[^8]: python-kraken-sdk documentation, Futures REST — `get_ohlc()` — https://python-kraken-sdk.readthedocs.io/en/v2.0.0/src/futures/rest.html (accessed 2026-07-21)
[^9]: Web search results describing `futures.kraken.com/api/charts/v1/{tick_type}/{market}/{resolution}`, its `more_candles` field, and resolution set (1m–1w) — search query "Kraken Futures API OHLC candles endpoint historical data docs.kraken.com futures-api charts" (accessed 2026-07-21); primary Kraken docs page it references (`docs.kraken.com/api/docs/futures-api/charts/candles/`) returned 404 on direct fetch, see confidence caveat above
