# Change 1 (one process per coin): built and proven (2026-11-16)

Branch `sd2/step4-per-coin` (worktree `wt/step4-per-coin`), from `ccr-6624e33e-aakrpv` at `cc19b01c9`. Committed and
pushed as `f1a8aa626` on the operator's go (2026-11-16); not yet merged into `ccr-6624e33e-aakrpv`.
Changed files:
- `04_backtest/helper/run_backtest.py`
- `04_backtest/card.md`
- new: `04_backtest/helper/test_run_backtest.py`

## What changed
- One `run_protocol.py` call per coin, on all its windows.
- That call is used only when every window has its own run folder: the summary lists the windows in order, the run
  ids are all different, and each folder has a `metrics.json`.
- Otherwise the coin is rerun one window at a time, exactly as before. This happens when the call failed (the wrapper
  stops at the first failing window) or two windows shared a folder.
- The call's own files (`protocol_summary.json.gz`, `trade_diagnostics.json.gz`, `engine_log.txt`) go in the coin's
  folder.

## Proof (this PC, Windows, 0 USD, no model call)
Today's helper (old) once, the new helper twice (new-1, new-2). All runs went into scratch folders.

| Case | Windows | Old | New-1 | New-2 | Gain | Coins on one call |
|---|---|---|---|---|---|---|
| `demo_run` e1 (all run) | 144 | 18.2 min | 7.6 min | 7.3 min | **-59%** | 6 of 6 |
| `full_data_run` 002-03 (3 windows fail) | 144 (141 run) | 17.7 min | 11.3 min | 11.2 min | -36% | 4 of 6 (XMR and XRP fell back, as designed) |
| `hourly_run` 001-01 (BNB has no data) | 18 (12 run) | 14.7 min | 11.9 min | 11.9 min | -19% | 2 of 3 (BNB fell back) |

| Check | Result |
|---|---|
| Per window, all 297 windows of the 3 cases: `metrics.json`, `forecast_distribution.csv`, `bars.csv` and `trades.json` (unzipped), `manifest.json` except `run_id`, `created_utc` and `git_sha` | **identical**: old vs new-1, old vs new-2 |
| Each window's entry in the coin's `protocol_summary` (252 entries) vs the old per-window summary | identical (`run_id` aside) |
| The coin's `trade_diagnostics` trades vs the old windows' trades, joined in order (14,099 trades) | identical |
| `INDEX.md`, `config.json`, `run.md` | identical, except 3 traceback lines in 002-03's `run.md`. They hold the path of the folder the engine ran from, and old and new ran from two different worktrees. Same line, same error. |
| Which windows failed, and why | identical: XMR w13, XRP w7 and w13 (warm-up check); BNB w1 to w6 (no data on the venue) |
| `metrics.json` and `forecast_distribution.csv` vs the committed records (written on the run machine) | identical (594 files) |
| new-1 vs new-2 | identical, except run ids and temporary folder names in the per-coin log and summary. Today's per-window files have the same kind of difference. |
| Step 5: the saved `measure.py`, run by step 5's own runner on old, new-1 and new-2 | same result in all 3 cases |
| Step 6: `check_profitability.py` on old, new-1 and new-2 | same `result.json` (e1, 002-03; `hourly_run` has no step 6) |
| Data files | none changed (`git status` clean in both worktrees) |
| Tests | 18 passed: the 8 new tests (clash, failed call, missing summary, wrong windows, missing metrics, the record with and without fallback), plus steps 5 and 6 and `common` |

## Reading
- **Results do not change.** Every file a later step reads is identical, and so are both verdict checks.
- **Gain on this PC:**
  - 59% when every window runs;
  - less when a coin falls back, since that coin is paid twice: about once for the failed call, plus once per window;
  - less on hourly bars, where start-up is a smaller part of a window.
- **Gain on the run machine: not known yet.** It runs Linux, where Python starts faster. Gate 0 in `3_plan.md`
  measures it there, or the journal's clock times at the first real run after the merge.
- **Possible later improvement, not built:** when a coin's call fails at window k, keep windows 1 to k-1 from that
  call and rerun only from k. This would cut the fallback's double cost. It is not needed for identical results.
