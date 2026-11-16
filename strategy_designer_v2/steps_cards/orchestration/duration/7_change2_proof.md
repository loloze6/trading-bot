# Change 2 (the coins at the same time): built and proven (2026-11-16)

Branch `sd2/step4-parallel` (worktree `wt/step4-parallel`), from `ccr-6624e33e-aakrpv` at `9bf353363` (change 1 and
the warm-up fixes in). Operator's go, 2026-11-16, with four conditions: the wrapper's setting is opt-in and off by
default; as many coins at once as the machine has cores, never a fixed 6; the proof as for change 1, then timing on
the run machine; merge only while no loop runs.

## What changed
| File | Change |
|---|---|
| `strategy-research/tools/run_protocol.py` | New setting `--trades-file-in-out-dir`, off by default: the engine's interim trades file goes to the call's own output folder instead of the one shared `trading-bot/results/trades.json`. That file only feeds `tradesxl.xlsx`; `trades.json`, `metrics.json` and `bars.csv` are written from memory. Without the setting, nothing changes. |
| `04_backtest/helper/run_backtest.py` | The coins run at the same time, as many at once as the machine has cores (the count Python reports: 8 on this PC, so all 6 coins). Step 4 always passes the new setting. `run.md` and `INDEX.md` list the coins in the plan's order. |
| `04_backtest/helper/test_run_backtest.py` | 3 new tests: never more coins at once than cores; the record keeps the coins' order whoever finishes first; each call gets its own trades file. |
| `04_backtest/card.md` | How it runs, point 5, with its "why this can't leak" note. |
| `POTENTIAL_ADJUSTMENTS.md` | Parked: two coins at once could rewrite the same data file (see below). |

**Not built:** the plan's data-file guard. The operator's rules (`CLAUDE.md`, rewritten 2026-11-16) say no gates. The
risk and a fix at its cause are parked for the operator.

## Proof (this PC, Windows, 8 logical cores; 0 USD, no model call)
Today's step 4 (`ccr` at `9bf353363`) once, the new helper twice (new-1, new-2). All runs went into scratch folders.

| Case | Windows | Old | New-1 | New-2 | Gain |
|---|---|---|---|---|---|
| `demo_run` e1 (all run) | 144 | 565 s | 233 s | 270 s | **-52 to -59%** |
| `full_data_run` 002-03 (XRP w13 fails, XRP falls back) | 144 (143 run) | 692 s | 379 s | 371 s | -45% |
| `hourly_run` 001-01 (3 coins; BNB has no data and falls back) | 18 (12 run) | 936 s | 657 s | 659 s | -30% |

Since the warm-up fixes, 002-03 fails on one window only (XRP w13; XMR w13 and XRP w7 now run), so its fallback is
tested on one coin. The hourly case gains less: 3 coins, and the slowest sets the time.

| Check | Result |
|---|---|
| Per window, all 299 windows: `metrics.json`, `forecast_distribution.csv`, `bars.csv` and `trades.json` (unzipped), `manifest.json` except `run_id`, `created_utc`, `git_sha`; which files each window folder holds | **identical**: old vs new-1, old vs new-2, new-1 vs new-2 (1,610 checks each) |
| The wrapper call's files (per coin, or per window on fallback): `protocol_summary` entries (299), `trade_diagnostics` trades (14,853), `engine_log.txt` with run ids, temporary folders and the worktree's name masked | identical |
| `INDEX.md`, `config.json`, `run.md` (the worktree's name in tracebacks masked) | identical |
| `metrics.json` and `forecast_distribution.csv` vs the committed records (the windows that exist there) | identical (594 files) |
| Step 5: the saved `measure.py`, run by step 5's own runner | same result on old, new-1, new-2 (3 cases) |
| Step 6: `check_profitability.py` | same `result.json` (e1, 002-03); `check.md` differs only in the line naming the scratch folder |
| The campaign's path: `run_protocol.py` without the setting, old vs new, on e1's config, BTC, fold A | the 6 windows' files identical (38 checks); the shared `trades.json` is written as before, with the same content |
| The shared `trading-bot/results/trades.json` during the new helper's runs | never written (it does not exist in the new worktree after 6 runs) |
| Data files | none changed (`git status` clean in both worktrees) |
| Tests | 45 card tests pass (11 for step 4). The campaign's 67 test files that name `run_protocol.py`: 2,269 pass, 14 skipped, 2 fail. The 2 fail on `ccr` without this change too: both look for `workflow_artifacts/skills/hypothesis-design/SKILL.md`, which is not there (`test_d186_forecast_ic_horizons.py`, the two prompt-assembler tests). |

## Why this can't leak
- The coins share no memory: each runs in its own processes, which read that coin's bars and the aux feeds, as when
  they ran one after another. Each window's own `run_backtest` call keeps its dates, warm-up and holdout guard.
- The files the processes share: the interim trades file (now one per call), the bot's log, and an aux data file the
  fetcher rewrites only when a read adds rows the file lacked (parked, above). None changed in the proof.
- Shown, not only argued: each window's data block in `manifest.json` (start, end, bar count, data hash) and its
  `bars.csv` are identical to today's step 4.

## Not done here
- **Timing on the run machine** (Linux container, 4 cores): the reviewer's, after the merge, as for change 1 (559 s
  before change 1, 288 s after). Check first how many cores Python reports there: in a container it can be the host's.
- **The merge** into `ccr-6624e33e-aakrpv`: only while no loop runs.
