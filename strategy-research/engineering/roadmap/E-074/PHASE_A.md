# E-074 phase A: exploration digest (code explores, the readers reason)

**Status:** design only, no code. Written 2026-10-08, autonomously (operator offline; he
reviews and merges). Each choice that belongs to the operator is under "Decisions for the
operator", with the default taken and the alternative.

**Ids used here:**
- E-074 (Linear P-CUL-82): this epic, the exploration digest.
- E-072 (P-CUL-80, PR #340, open): ideas are confirmed on windows the proposer never saw.
  It splits each run's windows into exploration and confirmation windows.
- E-073 (P-CUL-81, PR #342, open): the data dictionary of every field the AI steps read,
  with audit findings A1..A15.
- E-075 (P-CUL-83): the analyst pilot, a sixth reader that queries the data.
- E-027 / E-029: why a forecast is zero / the decision behind each trade (not built).
- CUL-394: automatic claim verdicts (parked); it holds the record of the significance
  methods that failed calibration.
- D-079: the operator's approval of the readers delivery plan (PR #339).
- "v3 readers": the five category readers of E-068 (profitability, trade efficiency,
  forecast power, regime power, component attribution).
- "claim-test DSL": the four-slot test language of `tools/claim_tests.py`
  (selector / outcome / baseline / statistic).

**Sources read:**
- the plan: `engineering/delivery_plan_readers.md` (PR #339), item 3 and "Decisions taken";
- the Linear project text of E-074;
- E-072: `engineering/roadmap/E-072/PHASE_A.md` and `tools/explore_confirm.py` on
  `origin/feat/e072-explore-confirm` at `f2ea26ec`;
- E-073: `docs/DATA_DICTIONARY.md` on `origin/feat/e073-data-dictionary`;
- the code on master `4d585c33` (line numbers below are on that commit unless marked
  "E-072 branch");
- the saved runs run_065 (1d), run_070 and run_074 (1h), read-only, from the main checkout.
  No data cache was opened.

---

## 1. What already exists, and how a digest cell maps onto the claim-test DSL

### 1.1 What `claim_tests` and `claim_measure` compute today

- A test is one sentence with four slots: "on these bars (selector), what happens next
  (outcome) differs from these other bars (baseline), measured like this (statistic)"
  (`tools/claim_tests.py:1-8`).
- Selectors (`claim_tests.py:530`, `SELECTORS`):
  - `all` (`:443`);
  - `event`: a bar-t field compared with a value (`:470`);
  - `regime`: the bar's regime label (`:483`);
  - `regime_change`: the bar where the regime switches to a label (`:490`);
  - `calendar`: weekdays and/or UTC hours of the bar's start time (`:500-509`);
  - `quantile`: a bar-t field in the top or bottom `q` of its trailing `lookback` bars,
    past only, `q` at most 0.5 (`:512-527`).
- `past_return` is not a selector. It is a bar-t **field** (with `bars: n`) that `event` and
  `quantile` read: close[t] / close[t-n] - 1, defined only when all n bars are in the same
  window (`:146-147`, `:448-459`).
- Outcomes (`:582`): `fwd_return`, `fwd_volatility`, `fwd_max_drawdown`, `trend_ends`, all
  matched by timestamp inside one window (`:539-579`).
- Baselines (`:633`): `complement`, `placebo`, `other_selector`.
- Statistics (`:699`): `mean_diff`, `rank_ic` (Spearman of the bar-t forecast with the
  outcome on the selected bars, no baseline), `hit_rate`, `decay_curve`.
- `effect_sizes` (`:1022-1061`) gives, per horizon: the pooled value, the per-window values,
  the per-era values and the event and block counts. It computes no p-value.
- `_prepare` (`:899-913`) returns, per window, the selector mask, the baseline weights, the
  outcomes per horizon and the forecast. That is exactly the per-row material a bootstrap
  needs.
- `claim_measure.measure_test` (`tools/claim_measure.py:178-217`) wraps `effect_sizes` and
  adds a per-coin split (`_per_coin`, `:132-152`: the same statistic restricted to one
  coin's windows) and the "claimed sign in k of n windows" count.
- `claim_measure.check_before_holdout` (`:113-119`) refuses any bar at or after the holdout
  start.
- E-072 already measures card tests on a chosen subset of windows:
  `explore_confirm.measure_on_windows` (E-072 branch, `tools/explore_confirm.py:403-423`)
  loads a variant's bars with `claim_tests.load_variant_bars` and keeps only the given
  window labels.

### 1.2 How a digest cell maps onto the DSL

A **cell** is one number, with its interval, for one (family, slice, horizon, variant,
coin). Two bar families and one trade family:

| Family | What it asks | Selector | Outcome | Baseline | Statistic |
|---|---|---|---|---|---|
| `forecast` | does the forecast rank the next h-bar return well inside this slice? | the slice (e.g. `calendar hours [13]`) | `fwd_return [h]` | none | `rank_ic` |
| `forecast_quantile` | what is the next h-bar return when the forecast is in quantile k? | `quantile field forecast` (k = 1 or 5) | `fwd_return [h]` | `complement` | `mean_diff` |
| `price` | is the next h-bar return different in this slice, whatever the forecast? | the slice | `fwd_return [h]` | `complement` | `mean_diff` |
| `trade` | is the net return of the trades in this slice different from the other trades? | (not a DSL test: see 1.3) | lot net return | the other lots | mean difference |

- Every `forecast` and `price` cell on an **extreme** bucket, a calendar slot or a regime is
  written as an exact DSL spec. The digest computes it through `claim_tests._prepare` /
  `effect_sizes`, and the cell carries that spec as `as_test`.
  - So a reader who wants to propose the cell as a side finding copies `as_test`. E-072 then
    confirms exactly the same definition on the confirmation windows
    (`explore_confirm.finding_route`: a price-only claim is measured in the same run).
  - A test pins this: `claim_measure.measure_test(as_test)` on the exploration windows gives
    the cell's value.
- **Interior buckets are not DSL tests:** forecast quintiles 2-4, the middle volatility
  tercile and past-return deciles 2-9.
  - `quantile` takes top or bottom `q <= 0.5` only (`claim_tests.py:777-784`).
  - The digest computes them with one internal band function. It uses the same trailing
    `np.quantile` thresholds as `sel_quantile`.
  - Those cells carry `as_test: none (interior bucket)`. Decision 9 covers exposing a band.
- The "forward return of forecast quantiles **by** slice" in the epic would need an AND of two
  selectors (forecast quintile AND hour 13), which the DSL does not have.
  - The default answers the same question with one DSL-native number per slice: `rank_ic`
    inside the slice, plus the forecast-quantile curve on all bars.
  - Decision 1 has the alternative.
- **Per coin:** every cell is computed on one coin's windows only, the `_per_coin` pattern
  (`claim_measure.py:132-152`).
  - There is no pooled cross-coin cell: coins have different volatility and move together,
    so a pool is neither comparable nor independent.
  - The `price` family depends only on the coin's closes, so it is computed once per coin,
    not once per variant.

### 1.3 What is missing

1. **Trailing volatility, a bar-t field.**
   - Definition: the sample std (ddof=1) of the n one-bar log returns ending at bar t (rows
     t-n .. t).
   - It is defined only where the bar stamped ts[t] - n*step is in the same window and all
     n+1 rows are present (row distance exactly n), the `past_return` rule
     (`claim_tests.py:448-459`). It is NaN elsewhere, including the first n bars of every
     window.
   - It is added as `trailing_vol` to `BAR_T_FIELDS` and `FIELDS_WITH_BARS`
     (`claim_tests.py:146-147`), so `event` and `quantile` can read it.
   - A guide line goes in `workflow_artifacts/skills/hypothesis-design/CLAIM_TESTS.md:110-121`,
     because `tests/test_e068_s2_claim_card.py:366-367` requires every field to be
     documented (decision 8).
2. **A band (interior bucket)** inside the digest only (above).
3. **A block bootstrap of a cell's statistic, and the chance line.**
   - Nothing in the running pipeline computes an interval. `claim_measure` is effect sizes
     only, by rule (CUL-394, `claim_tests.py:16-26`).
   - The digest adds a standard error. It never adds a verdict (section 3).
4. **The trade grid: `claim_tests` reads bars only** (`load_variant_bars`,
   `claim_tests.py:407-440`). The trade readers today:
   - `run_protocol._compute_trade_records_for_window` (`tools/run_protocol.py:570-669`)
     reads each window's `trades.json` and `bars.csv` and writes
     `variants/<vid>/trade_diagnostics.json` (`:2528-2545`);
   - `build_reports.build_trade_efficiency_report` (`tools/build_reports.py:454`) averages
     every numeric trade field per window, per regime and per symbol (`_aggregate_records`,
     `:212`; E-073 A10);
   - `fragment_patterns.py` and `portfolio_whole_test.py`, offline tools.
   None of them slices trades by entry hour, holding time, exit cause or the move before
   entry, and none gives an interval. The digest reads `trades.json` (it has `side`,
   `exit_forecast` and `matched_quantity`, which `trade_diagnostics.json` drops) plus the
   window's `bars.csv`, through the same `protocol_result.yaml` → `results[].run_id` mapping
   as `load_variant_bars`.
5. **An exit-cause label that is right** (section 4).

---

## 2. The cell list per timeframe, and the count on a real run

### 2.1 Fixed settings (pre-declared, by timeframe)

| Setting | 1h | 1d |
|---|---|---|
| Horizons h (bars) | 1, 24 | 1, 5 |
| `past_return` length n | 24 | 5 |
| `trailing_vol` length n | 24 | 10 |
| Trailing quantile lookback L (cut points from the past L values only) | 336 (14 days) | 30 |
| Bootstrap block B (bars) | max(2h, 24) | max(2h, 5) |
| Bar-cell floor | >= 100 bars with an outcome and >= 10 blocks | >= 30 bars and >= 6 blocks |
| Trade-cell floor | >= 30 lots | >= 30 lots |
| Holding-time buckets (bars) | 1 / 2-3 / 4-12 / 13+ | 1 / 2-3 / 4-10 / 11+ |

- **Bars lost at each window's start, with no warm-up read** (decision 13). A trailing
  bucket needs n + L earlier bars of the same window.
  - 1h: 360 of about 2,900 bars per window (12%).
  - 1d: 35-40 of about 120 bars per window (29-33%).
  - Measured window lengths: run_074 has 2,880-2,952 bars per 1h window; run_065 has
    120-123 per 1d window.

### 2.2 Slices

- **Calendar:** hour of day, 24 UTC hours of the bar's start (`sel_calendar`,
  `claim_tests.py:500-509`). The decision is taken at that bar's close, one hour later.
  1h only.
- **Weekday:** 7 days. 1h only, as the epic says (decision 3).
- **Regime:** one slice per label present with at least the floor (`trending`,
  `mean_reversion`, `chop`, `unknown`; `NOT_READY`, `ERROR` and empty labels excluded).
  - With fewer than 2 labels the family is empty, with the reason written: one label is
    the same as "all bars".
  - Every graded variant of run_065, run_070 and run_074 has the single label `unknown` on
    every bar (measured), so R = 0 on recent runs.
- **Volatility tercile:** 3 buckets of `trailing_vol` against its trailing L values.
- **Past-return decile:** 10 buckets of `past_return` against its trailing L values.
- **Forecast quintile:** 5 buckets of the forecast against its trailing L values.
  - If more than half of the valid bars have a forecast of exactly 0 (a sparse event
    signal), it is 3 sign buckets instead (short / flat / long).
- **All bars:** the overall forecast `rank_ic`.

### 2.3 Cells

Notation: V = graded variants, C = coins, H = horizons, R = regime slices.

| Family | Unit | 1h cells per unit | 1d cells per unit |
|---|---|---|---|
| `forecast` + `forecast_quantile` | per variant x coin x horizon | 1 all + 5 quintiles + 24 hours + 7 weekdays + R + 3 vol + 10 past-return = **50 + R** | 1 + 5 + R + 3 + 10 = **19 + R** |
| `price` | per coin x horizon | 24 + 7 + R + 3 + 10 = **44 + R** | R + 3 + 10 = **13 + R** |
| `trade` | per variant x coin | 24 entry hours + 4 holding + 5 exit causes + 3 pre-entry move = **36** | 4 + 5 + 3 = **12** |

- **Trade slices.**
  - Entry hour: the entry bar's UTC start hour (1h only).
  - Holding time: exit bar row minus entry bar row, matched by timestamp in `bars.csv`.
  - Exit cause: section 4.
  - Move before entry: z = side x past_return(n) / (trailing_vol(n) x sqrt(n)) at the
    entry bar, all from closes at or before the entry bar. Buckets: against the move
    (z < -1), neutral, with the move (z > 1). Fixed cut points, never sample quantiles.
- **Trade outcome:** the lot's net position return (`net_profit_loss_percent` in
  `trades.json`: commission out, slippage inside the fill prices), weighted by entry
  notional (decision 12).
  - The effect is the cell's weighted mean minus the weighted mean of the variant x coin's
    other lots.
  - A "trade" is one LIFO lot, not an entry-to-flat round trip (E-073 section "How to read
    it").
- **How many cells are DSL tests:**
  - 1h: 38 + R of the 50 + R forecast cells, and 35 + R of the 44 + R price cells. The
    others are interior buckets.
  - Trade cells: none.

### 2.4 Counts on real run shapes

- **run_074 (1h): 360 cells.**
  - Shape (measured from the saved run): 6 windows, 3 of them exploration under E-072's
    rule (2022-01, 2022-05, 2022-09).
  - Graded variants: `base` and `design_longer_smoothing`, both BTCUSD.
    `asset_xrp_generalization` was not graded (no `protocol_result.yaml`). R = 0.
  - forecast: 2 variants x 1 coin x 2 horizons x 50 = 200.
  - price: 1 coin x 2 horizons x 44 = 88.
  - trade: 2 x 36 = 72.
- **The same run with its XRP variant graded: 584 cells** (300 + 176 + 108).
- **run_065 shape (1d): 202 cells.** 3 graded variants on BTC, BTC and SOL, R = 0:
  - forecast: 3 x 2 x 19 = 114;
  - price: 2 coins x 2 x 13 = 52;
  - trade: 3 x 12 = 36.
- **For scale:** with K = 360 cells and 3 exploration windows, a cell with no effect shows
  the same sign in all 3 windows 25% of the time. That is about 90 cells by luck, which is
  why the sign count is never shown or ranked.

### 2.5 Size, and how it reaches the readers

- **Size: about 8,000 tokens for the 360-cell table** (estimate, not measured on a real
  digest). A mock of the proposed compact row format,
  `[family, slice, h, variant, coin, effect, ci_low, ci_high, n]`, is 27 KB for 360 rows.
- Plus about 2,000 tokens (estimate) for the header, the chance line and the shortlist.
- About 10,000 tokens per reader in total.
- For comparison, run_074's `reports/trade_efficiency.yaml` is 43.6 KB and all its reader
  inputs together are 122 KB (measured).

---

## 3. The chance line, and each cell's interval

### 3.1 What failed before (do not repeat)

- **CUL-394 / E-068 (`engineering/roadmap/E-068/REGRADE_run065.md:352-358`).** Three
  significance methods failed or were retired on edge-free simulated prices:
  - a circular shift of the signal: continuation claims 0.00-0.01, reversal claims
    0.10-0.12, hourly rank IC 0.00 / 0.33 (the signal is built from past prices);
  - a block-adjusted analytic p (`block_analytic_v1`,
    `E-068/calibration_block_analytic_v1.yaml`): hourly rank IC 0.000 in every cell, daily
    0.005-0.090;
  - chunks drawn with replacement (`bootstrap_null_v1`): finite-sample depletion bias.
- Only the block-permutation method B passed, for Donchian(20) daily only. It needs the
  forecast recomputed on fake prices by a vectorized copy of the component (`SIGNALS`,
  `claim_tests.py:232`; Donchian and Keltner only). The gate's price model is daily-only
  (CUL-394 item 8).
- **So no calibrated method exists for an arbitrary forecast on hourly bars.** Whatever
  the digest uses is uncalibrated and must say so.

### 3.2 Recommended: an expected-count sentence plus a Bonferroni line

- **Per cell:**
  - the effect;
  - its standard error (se) from a block bootstrap (3.3);
  - the 95% interval, effect ± 1.96 se;
  - `beyond_chance_line: true` when |effect| > z_K x se, where z_K is the two-sided
    Bonferroni z for K cells.
  - z_K: 3.81 for K = 360, 3.66 for K = 202, 3.93 for K = 584 (computed).
- **K counts every cell of the declared grid that was computed**, below-floor cells
  included: they were looked at.
- **The chance line, one paragraph at the top of the digest:**
  > "K = 360 cells were computed on the exploration windows. If no cell had a real effect,
  > about 18 (5% of K) would show a 95% interval excluding zero by luck alone. This digest
  > has M. The family line is |effect| > 3.81 se. If no cell had a real effect, the chance
  > that any cell crosses it is at most 5%, provided the standard errors are right. M_B
  > cells cross it. The standard errors come from a block bootstrap that is not calibrated
  > (CUL-394). Every cell is a lead for the confirmation windows, never a finding."
- **Why this one:**
  - It is the simplest method that holds whatever the dependence between cells.
  - The expected count (5% of K) is a sum of expectations, so it needs no independence.
  - Bonferroni bounds the chance of any false crossing under any dependence. Here the
    dependence is real: adjacent hours, nested horizons (h = 24 contains h = 1), near-twin
    variants, and three adjacent 2022 windows. So the line is conservative, never
    flattering.
  - It matches the epic's own analytic figure ("with about 24 cells, at least one shows 6/6
    by chance about 31%": 1 - (1 - 1/64)^24 = 0.315, checked) and the plan's rule that the
    CUL-394 bootstrap is un-parked only if the analytic figure is challenged.
- **What it can claim:**
  - Under the null, the number of cells beyond the 95% interval is about 5% of K on
    average.
  - A cell beyond the family line is unlikely to be luck within this digest, if its se is
    right.
- **What it cannot claim:**
  - That the se is right. The block bootstrap is not calibrated. Long-memory volatility or
    regime persistence longer than the block would make it too small, and then crossings
    flatter.
  - Anything about looks outside the digest: the readers' own tests and earlier runs. The
    E-072 ledger (`campaign_record/confirmations.yaml`) counts confirmation looks.
  - Anything beyond 2022. The three exploration windows sit in one era, one bear market.
  - That M a little above 5% of K means something. Correlated cells make the count lumpy:
    its spread is wider than binomial.
- **Power (estimate, assuming independent bars).**
  - Measured return spread on BTCUSD, exploration windows: 69 bps per hour (run_074 base,
    8,757 one-bar returns) and 335 bps per day (run_065 base, 362).
  - About 320 bars per hour-of-day cell gives se of about 4 bps, so the family line is
    about 15 bps per hour.
  - About 7,600 bars for the overall `rank_ic` gives se of about 0.0115, so the line is an
    IC of about 0.044.
  - About 80 bars per 1d tercile gives a line of about 140 bps per day.
  - **On one year of exploration data the line will usually be crossed by nothing.** That
    is the honest expected result. The shortlist still ranks leads for confirmation.
- **Alternatives considered (decision 4):**
  - Holm: same assumptions, slightly more power, a threshold that depends on the ranking,
    harder to explain.
  - Benjamini-Hochberg at 10%: it controls the share of false leads, not "any". It is
    defensible because E-072 is the real filter, but it is not the epic's "family-wise".
  - A max-statistic permutation over the whole family (Westfall-Young): it needs a null
    generator that keeps the dependence. The only calibrated one needs the signal
    recomputed per component, has no hourly gate, and costs about K times the digest.
    Parked with CUL-394.

### 3.3 The interval: a block bootstrap inside each window

- **Rows are resampled in blocks of B consecutive bars** (table 2.1). Each block stays inside
  one exploration window, and each window keeps its own block count (stratified by window).
  1,000 resamples, a fixed seed (`claim_tests.PLACEBO_SEED`, `:174`). se = std of the
  resampled statistic.
- **Why blocks of at least 2h:**
  - h-bar forward returns overlap for h > 1;
  - hourly returns cluster in volatility;
  - `claim_tests` already uses 24-bar (1h) and 5-bar (1d) blocks for its null
    (`BLOCK_BARS`, `:177`).
- `mean_diff` cells: per-block sums of the cell and the complement, resampled. That is
  cheap and exact.
- `rank_ic` cells: ranks are computed once on the full cell, then the resampled
  rank-pair correlation is computed (an approximation of re-ranking each resample; stated
  in the file).
- **Trade cells:** lots grouped by the B-bar block of their entry bar; groups resampled
  inside each window.
- **Runtime: under 2 minutes per run** (estimate, not measured).
- **Not by window:** 3 exploration windows give 2 degrees of freedom, which is useless. Not
  analytic HAC either: `block_analytic_v1` is the method that failed calibration.

### 3.4 Ranking

- **Within each family, cells meeting the floor are ranked by the end of their 95% interval
  nearest zero** (the smallest effect the data still allow), with the point effect shown
  beside it. Decision 6 has the epic's literal "by effect size".
- Families have different units (IC, bps per bar, % per lot), so there is no cross-family
  ranking.
- The **shortlist** holds the top 8 of each family, plus every cell beyond the family line.
  The full table follows it in the same file.
- The windows-with-the-same-sign count is never shown (decision 15).

---

## 4. Exit cause and MAE/MFE for the trade grid, without waiting for E-027

### 4.1 Today's label is not usable (E-073 A5, plus one new defect)

- `run_protocol._infer_exit_reason` (`tools/run_protocol.py:489-535`) returns `signal_flip`
  for every exit that is not at the window's end. Its flip test and its default both return
  `signal_flip` (`:530-535`).
- **New defect, not in E-073's list.** Its first end-of-window test compares **dates**:
  `exit_date >= window_end_date` (`:504-506`). On 1h bars the whole last calendar day of a
  window is labelled `end_of_window`.
  - Measured on run_074 base, exploration windows: 13 / 14 / 18 trades labelled
    `end_of_window` in `trade_diagnostics.json`, against 7 / 3 / 5 that exit on the last
    bar.
  - The later timestamp test (`:527-528`) is the correct one.
  - To be filed as an E-073 follow-up, not fixed here.

### 4.2 The digest's own classifier (per lot, in this order)

1. `end_of_window`: the exit bar is the window's last bar (timestamp equality, as
   `:527-528`). The engine's forced close is merged into that row (E-073 A15).
2. `flip`: `exit_forecast` has the opposite sign to the lot's side.
3. `to_zero`: `exit_forecast` is exactly 0 (not ready, an error, or a filter that outputs 0).
4. `reduction`: `exit_forecast` has the same sign and the position is still open after the
   bar (`postRebalance_current_allocation` in the exit row has the same sign, nonzero).
   This is a partial LIFO close by the rebalance.
5. `same_sign_flat`: `exit_forecast` has the same sign but the position is flat after the
   bar.
   - This is what a gap "large tier" forced flatten looks like.
   - Unexplained until E-027 records it; the label says so.
- `unknown`: no `exit_forecast`, or no exit row in `bars.csv`.

All inputs are known at the exit bar's close (`exit_forecast`) or its fill
(`postRebalance_current_allocation`).

- **Checked on run_074 base, exploration windows, 4,760 lots** (scratch script, read-only):
  - `reduction` 3,512 (73.8%);
  - `flip` 1,233 (25.9%);
  - `end_of_window` 15;
  - no `to_zero`, `same_sign_flat` or `unknown`.
- This agrees with E-073's review figure ("about 73% of run_074 base's exits are same-sign
  reductions").
- When E-029 records the decision behind each trade, this one function is replaced by that
  record (decision 10).

### 4.3 MAE / MFE: not used

- E-073 A6: they include the entry bar's own high and low, which happened before the fill at
  that bar's close (`run_protocol.py:306-325`; the holding slice starts at `entry_idx`,
  `:620-621`). Conclusions flip when the entry bar is excluded.
- They are also hindsight (`after`) fields. Slicing an outcome by another outcome invites
  rules that cannot be traded.
- The digest's only trade outcome is the lot's net return. Decision 11 has the alternative.

---

## 5. Where it is built, the flag, and what happens on a failure

### 5.1 Where

- At the `specialist_readers` stage, before the first reader, inside the flag-on branch of
  `_write_reader_v3_inputs`. This is right after
  `_write_exploration_reader_inputs` (E-072 branch, `run_phase1_research.py:5262-5266` calls
  it; body `:5436-5523`).
- Inputs:
  - the split (`explore_confirm.load_split`, E-072 branch `explore_confirm.py:309`);
  - each graded variant's `protocol_result.yaml`, `bars.csv` and `trades.json`, exploration
    windows only.
- Output: `artifacts/exploration/exploration_digest.yaml`. It is stamped as this attempt's
  copy with `explore_confirm.stamp_copies` (E-072 branch `:611-629`, which adds to the
  current attempt's list), so an earlier attempt's digest never passes as current
  (`current_copies`, `:632`).
- New module: `tools/exploration_digest.py`. Pure functions plus one writer, no flag read
  (the pattern of `explore_confirm.py`).

### 5.2 How it reaches the readers

- The handoff gains one optional input under the flag, in `_explore_confirm_handoff`'s
  pattern (E-072 branch `run_phase1_research.py:4491-4545`):
  `artifacts/exploration/exploration_digest.yaml`, given only when
  `current_copies` lists it.
- Plus one flag-on-only reader rule file, `readers_v3/DIGEST.md`, like E-072's
  `EXPLORATION.md`. It says:
  - what a cell is;
  - that the chance line comes first;
  - that `as_test` is the exact test to copy into a side finding;
  - that interior and trade cells have no exact test;
  - that `exit` fields describe outcomes and are never entry rules.
- All five v3 readers get it (decision 14). E-075's analyst reads the same file.

### 5.3 Flag and dependencies

- `orchestrator.exploration_digest.enabled`, off by default, in
  `config/campaign_config.yaml`, plus an entry in `config/feature_flag_register.yaml`
  (checked by `tests/test_feature_flag_register.py`).
- Reader: `run_phase1_research._exploration_digest_enabled()`. It raises on a non-bool and
  requires `orchestrator.explore_confirm.enabled`. That flag itself requires
  `reader_findings` and `variant_loop` (E-072 branch `:4098-4138`, using `_flag_dep`,
  master `:3301`).
- A wrong flag combination is a loud configuration error at the first read, as in E-072.
  It is not a mid-run stop.
- With the split `not_applicable` (fewer than 2 windows), there is no digest and the run
  proceeds exactly as with the flag off (`_explore_confirm_active`, E-072 branch `:5318`).

### 5.4 Never stop (E-072's pattern, D-080 / D-061)

- Any exception while building the digest is caught and logged loudly:
  - a partial file is removed;
  - the gap is recorded in `artifacts/reader_input_gaps.yaml` (`_record_reader_input_gaps`);
  - the readers run without it and are told it is missing (`_reader_v3_missing_inputs`).
- The digest is not in `_EXPLORATION_REQUIRED_COPIES` (E-072 branch `:5203`), so a missing
  digest never skips a reader.
- One variant whose bars or trades cannot be read gets `status: not_computed` with the
  reason. The other variants' cells are still written, and K counts only the cells
  computed.
- Information only: the digest never changes `idea_status`, the grid, routing or
  decide-next.
- **Flag off:** no file, and the handoff, the prompts and the stage are byte-identical
  (tested).

---

## 6. Why no cell can leak

- **Bar features are read at bar t only.**
  - Hour and weekday come from the bar's start timestamp. The decision is at that bar's
    close (E-073 "How to read it").
  - The regime is the bar-t label.
  - `past_return` and `trailing_vol` read rows t-n .. t of the same window, and are NaN
    when any row is missing.
  - The forecast is the bar-t forecast, known at the close.
  - Every bucket compares x[t] with cut points from the trailing L values t-L .. t-1 of the
    same window (`sel_quantile`'s rule, `claim_tests.py:512-527`). It is never a
    whole-sample quantile.
  - Trade-bucket cut points (holding time, the move z) are fixed numbers, not sample
    quantiles.
- **Outcomes come strictly after t:** close[t+h] matched by timestamp inside the same window
  (`out_fwd_return`, `claim_tests.py:546-551`). Nothing is chained across windows.
- **Trade entry features** (entry hour, the move before entry) use closes at or before the
  entry bar. The digest does not use `pre_entry_drift_pct`, because it is measured to the
  fill price (E-073 table 2).
- **Exit cause and holding time are outcome descriptors**, known at exit. They are labelled
  so in the file. They describe what happened to trades and are never a feature a
  strategy could read at entry.
- **Exploration windows only:** the digest reads only `split["exploration"]` labels (E-072's
  `measure_on_windows` pattern).
  - Test: changing every confirmation-window bar and trade leaves the digest byte-identical.
  - No confirmation-window label appears in the file.
- **Holdout:** `claim_measure.check_before_holdout` on every window read.
- **No data cache is read** (decision 13), so no row outside the run's own saved windows is
  parsed.
- **Hindsight in the bucketing itself:** none. The ranking and the chance line use the
  exploration cells only, and the confirmation windows stay untouched for E-072.

---

## 7. Slices (four small PRs)

1. **S1: the `trailing_vol` field** (`claim_tests.py`, `CLAIM_TESTS.md`).
   - Done when: `trailing_vol` with `bars: n` is accepted by `event` and `quantile`,
     computed as in 1.3, documented in the guide; existing spec hashes are unchanged.
   - Tests:
     - mutating any row after t leaves the value at t unchanged (lookahead);
     - NaN on the first n bars of each window and around a missing bar;
     - equal to a hand computation on a fixture;
     - `test_e068_s2_claim_card.py`'s documentation check passes.
2. **S2: the bar grid** (`tools/exploration_digest.py`: cell list, cells, bootstrap, chance
   line, ranking, writer).
   - Done when: given a run directory and the exploration labels, it writes the forecast,
     quantile and price families for 1h and 1d with the counts of section 2.
   - Tests:
     - exact cell counts on 1h and 1d fixtures (50 + R / 44 + R / 19 + R / 13 + R);
     - `as_test` reproduces each expressible cell through `claim_measure.measure_test`;
     - byte-identical output when confirmation-window bars change;
     - deterministic with the seed;
     - holdout refusal;
     - a smoke check on edge-free synthetic prices: the share of cells beyond the 95%
       interval is near 5%, and none or very few cross the family line. A sanity check,
       not a calibration gate.
3. **S3: the trade grid** (`trades.json` + `bars.csv`, classifier, buckets, notional
   weights, grouped bootstrap).
   - Done when: the trade family is written per variant x coin, 36 cells on 1h and 12 on 1d.
   - Tests:
     - the classifier on synthetic lots: flip, reduction, to_zero, same_sign_flat, last-bar
       end, and a last-day-but-not-last-bar exit that must NOT be `end_of_window`;
     - holding time from timestamps;
     - fixed buckets;
     - exploration-only mutation test.
4. **S4: wiring** (flag, register entry, config key off, the stage call, stamp, handoff
   optional input, `readers_v3/DIGEST.md`, never-stop).
   - Done when (the epic's own done-when):
     - the digest is produced, flag on, for a 1h and a 1d fixture run;
     - its cells use exploration windows only (tested);
     - the chance line is present;
     - flag off is byte-identical (handoff, prompts, stage).
   - Tests:
     - flag-off byte-identity;
     - the dependency raise;
     - `not_applicable` split gives no digest;
     - a builder exception gives a gap record and readers that still run;
     - a stale earlier-attempt digest is not given.
- S1 can be folded into S2 if the reviewer prefers three PRs.
- S2 and S3 do not depend on each other. S4 needs E-072 (#340) merged.

---

## 8. Decisions for the operator

Each has the default taken in this design, then the alternative.

1. **The forecast question per slice.**
   - Default: `rank_ic` inside the slice, plus the forecast-quantile curve on all bars.
     DSL-native, with no new grammar.
   - Alternative: a top-minus-bottom forecast-quintile spread inside each slice. That needs
     an AND of two selectors, digest-internal or added to the DSL.
2. **Hour granularity (1h).**
   - Default: 24 UTC hours (the epic's text). run_074: 360 cells.
   - Alternative: 6 four-hour blocks. run_074: 216 cells, smaller se per cell, blurred
     hours.
3. **Weekday on 1d runs.**
   - Default: off (the epic says 1h only).
   - Alternative: on, +7 cells per variant x coin x horizon and per coin x horizon. About
     50 daily bars per weekday cell on 3 windows, weak.
4. **The chance method.**
   - Default: the expected-count sentence plus a Bonferroni line, with block-bootstrap se
     (section 3.2).
   - Alternatives: Holm; Benjamini-Hochberg at 10% (more leads, controls the share of
     false ones, not "any"); max-statistic permutation (parked with CUL-394).
5. **The interval.**
   - Default: block bootstrap inside each window, B = max(2h, 24) on 1h and max(2h, 5) on
     1d, 1,000 resamples, fixed seed.
   - Alternative: analytic HAC (Newey-West) se. Rejected as default: the block-analytic
     method failed calibration (CUL-394).
6. **Ranking.**
   - Default: within a family, by the interval's end nearest zero. It is an effect size,
     and it demotes noisy small cells.
   - Alternative: by the point effect (the epic's literal text), with the floor only.
7. **Variants covered.**
   - Default: every graded variant.
   - Alternative: the base variant only (run_074: 224 cells instead of 360).
8. **`trailing_vol` in the readers' DSL.**
   - Default: yes, added to `BAR_T_FIELDS` and `CLAIM_TESTS.md`, as E-068 3b added
     `past_return` (`826c2ad8`), so a volatility lead can be proposed and confirmed by
     E-072.
   - Declared effect: `CLAIM_TESTS.md` gains one field. It is read only under
     `orchestrator.claim_tests`, so prompts with that flag on change by one line, whatever
     the digest flag says. With every flag off, nothing changes.
   - Alternative: digest-internal only. Prompts are untouched, and volatility leads stay
     `not_measurable` in E-072.
9. **Interior buckets.**
   - Default: computed by a digest-internal band; no DSL change; those cells say they have
     no exact test.
   - Alternative: add a band (`q_low`, `q_high`) to the `quantile` selector, a grammar
     change for the readers.
10. **Exit cause now.**
    - Default: the section 4.2 classifier from `exit_forecast` and the exit row's
      allocation, replaced by E-029's record when it lands. End of window means the last
      bar, not the last day.
    - Alternative: leave the exit-cause cells out until E-027/E-029 (trade family 31 / 7
      cells).
11. **MAE / MFE.**
    - Default: not used (A6 bias, hindsight).
    - Alternative: recompute them inside the digest from `entry_idx + 1`.
12. **Trade weighting.**
    - Default: lot returns weighted by entry notional, return per unit traded. Tiny
      rebalance lots weigh little; they are 74% of lots on run_074.
    - Alternative: every lot weighs the same.
13. **Warm-up.**
    - Default: no data cache read. 12% of 1h bars and about 30% of 1d bars are lost at
      window starts.
    - Alternative: read the warm-up rows before each window from the cache
      (`claim_tests.read_warmup`, past only, as the null does). More 1d bars, but a cache
      dependency.
14. **What the readers get.**
    - Default: all five readers get the whole file: chance line, shortlist, full table.
      About 10,000 tokens (estimate).
    - Alternatives: the shortlist only, or each reader only its lens's families.
15. **Per-window values.**
    - Default: not shown. Only the effect, interval and counts, so no "3/3 windows"
      reasoning.
    - Alternative: show each exploration window's effect.
16. **Settings of table 2.1** (horizons, n, L, floors, holding buckets).
    - Default: as listed.
    - Alternative: add a 1-bar `past_return` decile on 1h (the shock family): +10 cells per
      variant x coin x horizon and per coin x horizon.

## 9. Outside this epic

- **The `end_of_window` date defect (4.1).** File it as an E-073 audit follow-up. It
  affects `trade_diagnostics.json` and the trade_efficiency report today, flag-off.
- **Calibrating the digest's se on edge-free hourly prices.** This is CUL-394's hourly
  gate; un-park it only if the analytic line is challenged (the plan's rule).
