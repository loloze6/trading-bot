# Engine E12: an hourly book on gapped bars ran for more than a day (2026-11-27)

Branch `engine-e12` (from `ccr-6624e33e-aakrpv`, with `origin/build-a4-common` merged). Shared code: **not merged;
the merge is the operator's go.**

## The fault
In the common records (step 9), two hourly books of `retest_weekend_run` (026-04 …d1_heavy-weekend-extends-week_1h
and …d2_heavy-weekend-falls-continue_1h) ran for more than a day and were stopped with no record.

## The cause (measured, not the start-up)
Reproduced with step 4's own `run_part`, coin by coin, each engine call timed and stack-sampled (py-spy):
- Every coin's windows ran in normal time (XRP 27 windows: 9 min). **BTC's one call on its 32 windows did not end.**
- At 20 min its stack was in the wrapper's summary after the windows, not in the engine's start-up:
  `_build_extended_summary` → `_pooled_ic_with_bootstrap_fallback` → `stationary_block_bootstrap_ic_significance`.
- Why it goes there: this book is active one hour a week, so every window has fewer than 5 active bars and an
  undefined forecast/return correlation. The wrapper then pools the coin's bars over all its windows (93,205 BTC bars).
- Why it does not end: the bar step is read from the first window's first two bars, and on BTC that pair spans a
  3 h hole. So the step is taken as 3 h, nearly every hourly bar is its own "segment", and each of the 1,000
  resamples scans the segment list once per bar drawn (tens of thousands of draws, each scanning tens of thousands of segments, per resample; seen at 20 min: 50,336 of
  93,205 bars drawn in the current resample, in segments of 1 bar).
- What it was for: of this call, the wrapper keeps only the observed pooled correlation (computed once, on the real
  bars) and the method label. The resamples' p-value was computed and dropped.

## The fix
`ic_only=True`: the call returns the method and the observed pooled correlation, with no resamples. This is the same
pattern as `episode_significance.method_only` (topic 33). Files:
- `trading-bot/performance/signal_statistics.py`: the `ic_only` option (default off: every other caller is unchanged).
- `trading-bot/backtest/run_protocol.py`: its one caller asks for `ic_only`.
- `trading-bot/tests/test_pooled_ic_fallback_gapped_hourly.py`: 3 tests. `ic_only` gives the full call's value and
  method (3 step cases, and an undefined correlation); the stalled case at its real size (32 windows, 93,000 hourly
  bars, a first pair over a hole) ends in under 20 s. **Without the fix it hits the 120 s limit.**

**Why this can't leak:** no data is read differently; the change drops a computation whose result was not used.

## Proof (fixed inputs, before and after)
Step 9's own `backtest()` on the common windows (`research_2016`), with the code before the fix (a worktree at
`d22dd30`) and after it (`9aee4f8`):

| Book | Bar | Coins | Before | After |
|---|---|---|---|---|
| night8 060-01.g1.d2.d1 own-range close-height fade | 1d | BTC ETH XRP ZEC | 364 s | 329 s |
| night4 024-02…d1 fading dip in uptrend | 4h | BTC ETH XRP ZEC | 654 s | 597 s |
| night4 028-04…b1 quiet dip in uptrend recovers | 1h | BTC ETH XRP ZEC | 679 s | 664 s |
| retest_weekend 026-04…d1 heavy weekend extends week (the stuck book) | 1h | ETH XRP LTC | 774 s | 668 s |

**2,956 files on each side, the same names; 1,953 byte-identical.** The 1,003 others differ only in:
- the engine's run ids and creation times;
- the git sha in the manifests;
- the temporary folder paths (`engine_log.txt`, `protocol_summary.json.gz`, the tracebacks in `run.md`);
- the plan's path in `run.md`, because the old code ran from another folder.

With those masked, every file is identical: bars, trades, metrics, windows refused and their reasons.
**Not covered by this proof:** none of these calls takes the fixed path. It is taken only when every window's
correlation is undefined, and the stuck book on XRP has 25 of 27. The fixed path is covered by the tests above
and by the two records below (BTC: all 32 windows undefined).

## Tests
`cd trading-bot && VENV -m pytest -q`: **1684 passed, 16 skipped** (the 3 new tests included).

## The two records (run on `engine-e12`, with the unmerged fix)
**These records depend on the fix, which is not merged.** Run with
`common_record.py --register --shard 1/1 --only <the two keys>` (4 cores). Both finished; before the fix, neither
finished in more than a day.

| | …d1 heavy weekend extends week (1h) | …d2 heavy weekend falls continue (1h) |
|---|---|---|
| Time | **2,732 s** (46 min) | **2,491 s** (42 min) |
| Coins that ran / asked | 16 / 25 (the 9 others have no 1h file) | 16 / 25 |
| (coin, window) pairs run | 289 | 289 |
| BTC (the stalled coin) | 32 / 32 windows | 32 / 32 |
| Step 5 on the common data | **confirmed** (main 0.0142, t 3.10, 600 cases) | **confirmed** (main 0.0166, t 5.16, 316 cases) |
| Step 6 on the common data | **not profitable enough** (Sharpe +0.97, minus holding −0.13, Calmar +0.96) | **not profitable enough** (Sharpe +0.46, minus holding −0.64, Calmar +0.40) |

The pairs not run are the engine's existing rules, written per window in `run.md`: the warm-up is too short at a
coin's first windows (LTC 3, ETH 1: "strategy not ready after 516 warm-up bars, required_bars=1441"), or the dates
were not fetched (2 at the start of 11 coins).

Committed, per `BUILD_A4_COMMON.md`, the small files only (25 files, about 9 MB, almost all of it the two
`chart_bars.csv.gz`): the record json and the INDEX line, `run.md`, `config.json`, the chart files, and the step 5
and step 6 results and indexes. Not committed: the per-coin `<SYMBOL>/wK/` and `windows/` folders (about 20 MB).
