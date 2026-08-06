# 2026 Coverage Gap — What Conversion Actually Remains

DISPATCH B1-R. Read-only. No run, no code, no conversion, no commit. No file inside the
holdout range `2026-01-01..2026-06-30` was opened, read, headed, parsed, or sampled; all
2026-range facts below come from filenames, sizes, counts, the registry, or a prior
written record, never from data. In-sample timestamp spans were extracted with
`awk -F, '{print $1}'` (field 1 only); no price, volume, or trade-count value was
emitted at any point.

## Manifest

| Check | Required | Found | Result |
|---|---|---|---|
| `git log --oneline -1` | starts `fec0120` | `fec0120 gitignore hygiene for external publication…` | PASS |
| `git status --porcelain \| grep -v '^??' \| wc -l` | `0` | `0` | PASS |
| `git status --porcelain \| grep -c '^??'` | 92 (informational) | `92` | matches |

Manifest holds; proceeded to step 2.

## Step 2 — The 2026 Requirement

Verbatim from `strategy-research/config/campaign_data_policy.yaml`:

- `:18` — `holdout_range: ["2026-01-01", "2026-06-30"]`
- `:8-9` — *"holdout_range: FROZEN — no stage, tool, prescreen, or diagnostic may read
  candles inside this range except the (future) holdout_evaluation stage."*
- `:62-65` — the only era covering 2026:
  ```
  - era_id: era_2026_holdout
    range: ["2026-01-01", "2026-06-30"]
    feeds_available: [ohlcv, fear_greed, funding_rate]
    note: matches holdout_range above. FROZEN — same holdout rules apply.
  ```
  The prior era `era_2024_2025_walk_forward_extension` (`:58-61`) ends `2025-12-31`.
  **No era is defined for `2026-07-01` onward.**
- `:161-168` — the tranche entry (key is `kraken_q1_2026_holdout`):
  ```
  quarantined: "2026-07-24"
  source_dir: local_data/holdout_sealed/2026_H1/kraken_q1_2026/
  era: era_2026_holdout
  span: ["2026-01-01", "2026-03-31"]
  sealed: true
  single_use: true
  status: sealed_holdout_not_reachable
  ```
- `:192` — `holdout_consumed_by: []` → **the holdout is entirely unspent.**
- `:199` — `holdout_failure_is_terminal: true`

| Range | Frozen? | Sealed? | Note |
|---|---|---|---|
| `2026-01-01` → `2026-03-31` | YES (`:18`, `:63`) | YES (`:166-167`) | Q1 tranche physically quarantined |
| `2026-04-01` → `2026-06-30` | YES (`:18`, `:63`) | **NO** | Frozen but *nothing to seal* — no Q2 data exists anywhere |
| `2026-07-01` → present | **NO** | NO | Neither. Outside `holdout_range`; no era defined; no Kraken data on disk |

The Q2 row is load-bearing: frozen *and* empty. Sealing and availability are not the
same property, and only Q1 has both.

## Step 3 — What Exists for 2026 Outside the Seal

**Finest available granularity for the Kraken pairs is 1h.** No Kraken `1d` cache
exists at all; `local_data/` root holds exactly 19 `kraken_{BASE}USD_1h.csv` files
(AAVE ADA AVAX BTC DOGE ETH INJ LINK LTC NEAR ONDO SOL SUI TAO TRX UNI XMR XRP ZEC).

Measured today per file (`awk -F, 'NR==2{print $1}'`, `awk -F, 'END{print $1}'`,
`awk 'END{print NR-1}'`): **all 19 terminate at the identical bar `2025-12-31 23:00`.**
First timestamps span 2013-10-06 (BTC) to 2024-07-01 (TAO); row counts 13,159 (TAO) to
96,381 (BTC). Not one file contains a single 2026 row — confirming
`campaign_data_policy.yaml:96-116` and `:74-76` exactly.

> **For the Kraken pairs, `2026-01-01 00:00` → present (`2026-07-26`) has ZERO
> daily-or-finer OHLCV coverage outside the seal. The entire year to date is a hole.**

Only `2026-01-01`→`2026-03-31` is backed by anything at all (the sealed tranche,
unreadable). `2026-04-01` → present is backed by **nothing, anywhere**.

### Seam claim: PARTIALLY CONFIRMED, and materially mis-framed

Claim: *archive ends 2025-12-31 23:00, first live bar 2026-06-22 23:00, ~4,151-bar hole.*

- **Archive side — CONFIRMED from files.** `2025-12-31 23:00` is exact and identical
  across all 19 pairs.
- **Live side — NOT a file fact and NOT static.** `2026-06-22 23:00` is the floor of
  Kraken's public OHLC endpoint's **fixed 720-bar rolling window**, not the start of any
  file on disk (`NEXT_SESSION.md:117-120`; `PIPELINE_IMPROVEMENTS_20260712_v4.md:2076-2078`
  records `n=721 first=2026-06-22 23:00 last=2026-07-22 23:00`, invariant under the
  `since` parameter — which is what makes it a rolling window, not a data boundary).
- **Correction.** That floor advances with wall-clock, so `4,151` is a snapshot valid
  **as of 2026-07-22/23**, not a standing quantity. As of today the floor would sit near
  `2026-06-26` and the gap near **4,247 bars**. *This is arithmetic, not a measurement* —
  I did not re-measure, because that requires a live fetch returning holdout-range bars.
  The original figure is internally consistent (173 days = 4,152 h → 4,151 bars strictly
  between); it is only stale.

### Holdout-range rows present in the in-sample cache root (finding)

Five committed root CSVs carry rows inside `holdout_range`: `BTCUSDT_1h.csv` and
`ETHUSDT_1h.csv` (both last `2026-07-05 10:00`, 74,457 rows), `BTCUSDT_1d.csv` and
`ETHUSDT_1d.csv` (both last `2026-03-19`, 3,137 rows), `fear_greed_daily.csv` (last
`2026-07-05`, 3,073 rows). These sit in the default, un-prefixed Binance cache slot
every `CcxtFetcher` consumer reads. This is **disclosed** — `NEXT_SESSION.md:124-131`
records the "Binance-future-holdout carry-forward" as deliberate — but it is **not** in
`campaign_data_policy.yaml` (which addresses only the Kraken pairs' non-reachability at
`:73-84`) and **not** in `local_data/README.md`. The registry's `:8-9` prohibition is
therefore protocol-only for these files: nothing physically stops a loader from reading
straight through 2026 H1. Reported, not remediated.

## Step 4 — Is the Sealed Tranche Already OHLCV? **YES.**

Established from filenames, sizes, counts, the registry and the README; no file under
`holdout_sealed/` was opened.

- **Layout.** `holdout_sealed/2026_H1/kraken_q1_2026/`, flat, **10,269 files, 1.9 GB** —
  matches `campaign_data_policy.yaml:152` ("~10,269 CSVs") and `:163` exactly.
- **Naming.** Suffix histogram: 1,467 files each at `_1`, `_5`, `_15`, `_60`, `_240`,
  `_720`, `_1440` — 1,467 × 7 = 10,269, a complete pair × resolution grid. The form
  `{KRAKEN_TICKER}_{RESOLUTION_MINUTES}.csv` is precisely the Kraken bulk **OHLCVT**
  convention documented at `local_data/README.md:88-91`; the Trades export uses
  `{PAIR}.csv` with no suffix (step 5), so the two are distinguishable by name alone.
- **Registry states the format.** `campaign_data_policy.yaml:152` names the tranche's
  original directory `Kraken_batch/kraken_ohlcvt_q1_2026` — **OHLCVT**, on the record.
- **Size corroborates.** `0GEUR_1440.csv` = 4,631 bytes. At daily granularity over Q1
  2026 (90 days) that is ≈51 bytes/row — consistent with 7 comma-separated numeric
  columns, inconsistent with a 6-column trades record.
- **Deviation noted.** The tranche has **no `_30` interval** (0 files), while `master_q4`
  has 1,403. Cosmetic here — `_1440` is present, which is what a daily consumer needs.

**Consequence: no aggregation is required to obtain Q1-2026 daily bars.** They already
exist, in final form, sealed.

## Step 5 — The q1_26 Tick Archive: **SUPERSEDED**

- **Location.** `trading-bot/local_data/Kraken_batch/q1_26/` — holdout-range data stored
  inside the in-sample tree.
- **Size / count.** **5.4 GB, 1,467 files**, all `.csv`; matches `README.md:64` exactly.
  Largest: `XBTUSD.csv` 326,605,146 B; `EURUSD.csv` 205,964,187 B.
- **Filename-inferred span: NONE.** Names are bare `{PAIR}.csv` — no date, no resolution
  component. The Q1-2026 span is known only from the directory name, `README.md:64-65`,
  and `campaign_data_policy.yaml:165`. Whether contents extend past `2026-03-31` is
  **not establishable without opening holdout-range data.**
- **Format.** Already on the record, verbatim, at
  `PIPELINE_IMPROVEMENTS_20260712_v4.md:2250-2251`:
  `Price,Volume,Timestamp,Type,Miscellaneous,Trade ID` — Kraken *Trades*, explicitly not
  the 7-column OHLCVT schema. Cited from that prior record; no file opened.
- **Supersession — decisive.** Pair universes compared **by filename only** (`comm` on
  the two sorted name lists): q1_26 = 1,467 pairs; sealed `_1440` set = 1,467 pairs;
  **only-in-q1_26 = 0, only-in-sealed = 0, in-both = 1,467.** Identical universe, same
  quarter. All 19 breadth-set pairs are present in the sealed 1440 set (checked with
  Kraken legacy tickers: `XBTUSD`, `XDGUSD` → both found).

> **q1_26 is the only source for nothing.** Every pair-quarter it covers already exists
> as finished OHLCVT at seven resolutions in the sealed tranche. Its sole residual value
> would be sub-1-minute reconstruction, which no campaign stage requires.

## Step 6 — The Conversion Path — Bucket: **SMALL (<3h)**, and almost certainly moot

### `data_manager.py:637` `.resample()` — NOT a candidate

Line numbers verified against the current 992-line file. The block at `:632-638` sits
inside the aux-feed pre-merge:
`.set_index("timestamp").resample(f"{self.interval_seconds}s").agg({name: feed.agg})`,
then `merge_asof` onto the price frame (`:640-645`). It downsamples **one named scalar
column** with **one** aggregation function (e.g. funding-rate 8h → bar interval), so it
cannot emit OHLC, which needs first/max/min/last/sum across five columns. The line-637
pointer in `NEXT_SESSION.md:135` points at the aux-feed resampler, not at an aggregator.

### `CandleBuilder` — the actual fit

`class CandleBuilder` (`:135`), docstring *"Aggregates price ticks into fixed-interval
OHLCV candles"*. Entry points `add_tick(PriceTick)` (`:165`) and `add_row` (`:174`);
state machine `_ingest` (`:236`); `_open_candle` (`:278`) seeds o/h/l/c from the first
tick; `_update_candle` (`:294`) does `high=max`, `low=min`, `close=price`, `volume+=`,
`tick_count+=1`; `_align` (`:302`) epoch-floors to the interval boundary. Inputs today:
`(symbol, price, volume, timestamp)` per tick. Output: a `Candle` carrying
o/h/l/c/volume/`tick_count`/`start_time`/`end_time`.

Three properties make it an unusually clean fit for a Trades → OHLCVT job:
`tick_count` (`:299`) maps directly onto Kraken's 7th column `trade_count`;
`candle_completion_callback` already **defaults to `None`** (`:154`, `:159`), so batch
use needs no decoupling from the strategy pipeline; and it emits a bar **only for
intervals that received ticks**, matching Kraken's own convention — *"the OHLCVT data
only includes entries for intervals when trades happened"* (`README.md:94-96`) — so no
empty-bar reconciliation is needed.

**What would have to be built** (none of it algorithmic): a Trades-CSV reader mapping
`Price,Volume,Timestamp` → `PriceTick`; a loop over 1,467 files; a headerless 7-column
writer; chunked reads for the 326 MB `XBTUSD.csv`; and a bound on `completed_candles`,
an unbounded `defaultdict(list)` (`:158`) that would otherwise hold every bar of every
pair in memory.

**Bucket evidence — SMALL.** The aggregation semantics exist, are exercised on both the
live and backtest paths, and need no modification; what remains is I/O plumbing. A
pandas one-liner (`.resample(…).agg({'price':'ohlc','volume':'sum'})`, native `ohlc`
aggregator) is shorter and far faster than per-row `add_tick` calls over hundreds of
millions of trades, and would shrink the estimate further.

**Two caveats outrank the estimate.** (1) The input is holdout-range data, so this is not
schedulable now at any size — this sizes the *mechanism*, not permission to run it.
(2) Per step 5 it would regenerate data that already exists in finished OHLCVT form.
`PIPELINE_IMPROVEMENTS_20260712_v4.md:2136-2140` anticipated exactly this: *"If Q1+Q2
2026 exist, the seam closes… This is by far the cheapest path and should be checked
before any aggregation work is commissioned."* Q1 now exists; that check has now been
made, and it comes back **do not commission the aggregation.**

## WHAT REMAINS

1. **Q2 2026 (`2026-04-01` → `2026-06-30`) is frozen and empty.** No Kraken data for it
   exists on disk in any form — not sealed, not tick, not OHLCV. Aggregating q1_26 cannot
   produce it; only a `Kraken_OHLCVT_Q2_2026` bulk export would, and its existence is
   unconfirmed (`PIPELINE_IMPROVEMENTS_20260712_v4.md:2130-2135`; sources index only
   through Q4 2025). **This, not conversion, is the real gap.**
2. **`2026-07-01` → present is unclassified.** Outside `holdout_range`, covered by no era
   (`campaign_data_policy.yaml:43-65`). Kraken's live endpoint reaches back only ~720
   bars and that window's floor currently sits *inside* the holdout, so any live top-up
   would pull holdout-range bars. The seam does not close from the live side without a
   policy decision first.
3. **Tick→OHLCV conversion is off the critical path** — SMALL, superseded, Q2-incapable.
4. **q1_26 sits in the in-sample tree.** 5.4 GB of holdout-range data under
   `Kraken_batch/`, whose sibling `master_q4/` *is* an ingest source
   (`ingest_kraken_archive.py:281`). The registry's reachability re-check (`:156-160`)
   covers `holdout_sealed/**` only; it does not assert non-reachability for `q1_26/`.
   Quarantining it alongside the sealed tranche is unresolved. Not actioned here.
5. **Five committed root CSVs carry holdout-range rows** (step 3) — disclosed in
   `NEXT_SESSION.md:124-131`, absent from both the registry and the README.
6. **The 4,151-bar seam figure is stale by construction** and should carry its as-of date
   (2026-07-22) wherever restated, or be replaced by the fixed archive-side fact plus
   "live window floor = now − 720h".

## REGISTRY–README DISAGREEMENTS

**No contradiction found.** Every quantitative README claim checkable against the
filesystem or the registry holds: `Kraken_batch/` 25,522 files (`:55`) → 25,522;
`holdout_sealed/` 1.9 GB (`:57`) → 1.9 GB; `master_q4/` 12,027 files (`:62`) → 12,027;
`q1_26/` 5.4 GB / 1,467 files (`:64`) → both exact; `Kraken_funding_rates/` 480 CSVs /
436 MB (`:56`) → 480 in `exports/`, 436 MB; `BTCUSDT_1m.csv` 177,664,416 bytes (`:58`) →
exact. The q1_26 Trades-not-OHLCVT characterisation (`:64-65`) is consistent with
`PIPELINE_IMPROVEMENTS_20260712_v4.md:2250-2251`, and the holdout/terminality/seal
citations (`:15-21`) match `campaign_data_policy.yaml:18`, `:199`, `:151-168`.

Two **gaps** (omissions, not conflicts) worth recording. First, **README §3 does not
disclose the holdout-range rows in the files it lists as published** — `BTCUSDT_1h.csv`,
`ETHUSDT_1h.csv`, `BTCUSDT_1d.csv`, `ETHUSDT_1d.csv` and `fear_greed_daily.csv` all
extend past `2026-01-01` (step 3), so §2.3's `end_date="2025-12-31"  # STOP HERE — 2026
H1 is the frozen holdout` (`:146`) reads as describing a boundary the cache has already
crossed; the registry is silent on it too, so neither document contradicts the other —
both are incomplete. Second, **README `:83` lists interval 30 among Kraken's OHLCVT
resolutions** while the sealed Q1 tranche contains none (`master_q4` has 1,403); the
README describes Kraken's product rather than this tranche, so this is imprecision
rather than error.

Neither file was edited.
