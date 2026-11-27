# Build A4, part 4: step 9, a candidate's common record (2026-11-26)

Branch `build-a4-common`, from `80957b2e84`. Design: `common/data_use.md` (sections 1 to 5 and 7, part 4), the
operator's go of 2026-11-26. Card: `orchestration/common_record/card.md`.

## Purpose and expected outcome (written before the build)
**Purpose:** every candidate gets one record on the same data: the 25 portfolio coins over the 32 windows of
`04_backtest/windows/research_2016.json`, a coin in a window only after its first 90 days. Steps 10 to 12, built by
another session, read these records.

**Expected:**
1. A function `orchestration/common_record/` (card, helper, tests) that writes the record, step 5, step 6 and a result
   file under the fixed paths, with one index line per record.
2. `run_idea` calls it for a candidate only in the data-use mode (`orchestration/loop/<run>/data_use.json`,
   version 2); without that file, `run_idea` writes the same files as before.
3. A batch entry over the register's paying books (`--register --shard i/n`), resumable.
4. Two records run (night 8's 060-01.g1.d2.d1 and 058-03.e1), with their times and an estimate for the 120 books
   in 6 shards.
5. No change to `trading-bot/`; the final coins never read; both test suites pass.

## What was built
| File | What |
|---|---|
| `orchestration/common_record/card.md` | the function's card |
| `orchestration/common_record/helper/common_record.py` | one plan, or `--register --shard i/n [--only KEYS]` |
| `orchestration/common_record/helper/test_common_record.py` | 7 tests (no backtest, no model call) |
| `orchestration/run_idea/helper/run_idea.py` | `data_use_version(run)`; the `common_record` step after step 6 and the chart files, for a candidate, only with version 2 |
| `orchestration/run_idea/helper/test_run_idea.py` | 1 test: no call without the file or with version 1; called right after the chart files with version 2 |

**How step 4 runs on the common data.** `run_backtest.py --coins C --windows F` runs every window for every coin, so it
cannot leave out a coin's first 90 days. Instead, the helper calls step 4's own functions, unchanged
(`run_backtest.protocol` and `run_backtest.run_part`), once per coin. Each call gets the coin's usable windows and the
number of windows before them, so `wK` is the K-th window of the file for every coin (step 6's "one window left out"
needs the same K to mean the same dates). `run.md` and the index line have step 4's shape. Step 4's code is not
changed, which avoids conflicts with build part 3, which changes step 4.

**The fixed interface** (told to the part-5 session, which read it the same way):
- `04_backtest/<run>/common/backtests/<id>/`: `run.md`, `config.json`, `<SYMBOL>/wK/`, `chart_bars.csv.gz` and
  `chart_trades.csv.gz` (today's format, committed names).
- `05_verification/<run>/common/verdicts/<id>/`.
- `06_profitability/<run>/common/checks/<id>/`.
- `orchestration/common_record/<run>/<id>.json`: plan, run, id, record, windows_file, coins_asked, coins_run,
  coin_windows, windows_run, step5, step6 (status, measures, informative), seconds, made_utc, commit. This file is
  written last, so a record whose json exists is complete.
- `orchestration/common_record/INDEX.md`.

## The two records
| | 060-01.g1.d2.d1 (own-range close-height fade) | 058-03.e1 (calm-rise stretch, ten days) |
|---|---|---|
| Time (4 cores) | **881 s** | **776 s** |
| Coins that ran / asked | 25 / 25 | 25 / 25 |
| (coin, window) pairs: ran / after the 90 days | 375 / 466 | 375 / 466 |
| Step 5 on the common data | inconclusive (t 1.89) | **confirmed** (t 3.12) |
| Step 6 on the common data | **not profitable enough** (Sharpe 0.59, minus holding −0.35, Calmar 0.37) | **profitable enough** (Sharpe 1.20, minus holding +0.25, Calmar 0.78) |
| Step 6 in-sample (6 coins, folds A to D) | profitable enough (Sharpe 0.69, minus holding +0.12, Calmar 0.81) | profitable enough (Sharpe 1.04, minus holding +0.47, Calmar 0.95) |
| Committed size | about 2 MB (1,457 files) | about 2 MB |

**Finding: the 91 pairs not run, 20 % of each record, are each coin's first usable windows.** The engine refuses them
for lack of warm-up: "strategy not ready after 142 warm-up bars, required_bars=395", or "the dates were not fetched"
when the warm-up reaches back before the coin's file. This is the engine's existing rule, the same as in research. It
is written per window in `run.md` and is not dropped. So for these plans the warm-up, not the 90-day rule, decides
where a coin starts: about 1 to 2 years after its first day. Example: BCH has 26 windows after its 90 days and ran 20.

## Estimate for the register's 120 paying books
97 daily, 10 on 4h, 13 on 1h. Daily is measured: about 830 s each. 4h and 1h are scaled from their in-sample step 4
times (journals: median 156 s daily, 139 s 4h, 449 s 1h, on 6 coins); this is not measured, and the 1h records have
fewer coins with hourly files.
| | Books | Per book | Total |
|---|---|---|---|
| 1d | 97 | about 830 s (measured) | about 22 h |
| 4h | 10 | about 750 s (scaled) | about 2 h |
| 1h | 13 | about 2,400 s (scaled, an upper bound) | about 9 h |
| **All** | 120 | | **about 33 h of a 4-core machine** |

**6 shards:** about 5.5 h each when each shard has its own 4-core machine (session). On one machine, 6 shards gain
nothing: each record already uses the 4 cores. Shard i takes books i, i+6, ... in the register's key order, so the
hourly books are spread across the shards. The two records above already exist and are skipped.

## Proofs
1. **Tests:** `VENV -m pytest -q strategy_designer_v2/steps_cards`: **183 passed**; `cd trading-bot && VENV -m pytest -q`:
   **1677 passed, 16 skipped**.
2. **`run_idea` without `data_use.json` is unchanged.** Night 8's plan 060-01.g1.d2.d1 was run twice from the same
   inputs: once with `run_idea.py` of `80957b2` and once with this branch's. Each used a fresh run seeded with the
   plan, the verdict and the step 7 outputs, so steps 3, 5 and 7 made no model call. Steps 4, 6, the chart files,
   the similarity check and the unseen test ran for real, and the similarity register was restored between the two
   runs. Compared file by file, the run name made the same in both: **2,127 files; 1,853 byte-identical.** The 274
   that differ differ only in these allowed fields:
   - the engine's run ids and creation times;
   - the git sha in the manifests;
   - the temporary folder paths in `engine_log.txt` and `protocol_summary.json.gz`;
   - the journal's times and seconds, and the order in which the parallel step 7 lines finished;
   - `finished_at` and the minutes in the table;
   - the register's `added_utc` and git sha.

   Every bar, trade, metric, verdict, check, chart file, comparison and unseen result is identical. The same steps ran
   in both, and `common_record` was not called.
3. **The final coins:** a test checks that the 90-day rule reads only portfolio coins and that the helper's code never
   names the final group (`test_the_final_coins_are_never_read`).
4. **`trading-bot/`:** not changed. `campaign_data_policy.yaml` and `local_data/holdout_sealed/` were not opened.

## Seen during the build (for the operator, not changed)
- The cards' test suite rewrites `topics/47_review/fold_rules_test.csv`: pytest collects `fold_rules_test.py` by its
  name. This predates the build; the file was restored before commit.
- Record 058-03.e1's `commit` field reads `d5beb4f…-dirty`: the commit was read after the steps had rewritten their own
  tracked index files. The field is now read before any write, but the record was not rerun.
- The 1h books would make larger records: a 6-coin 1h chart file is up to about 6 MB today.
- The data rules for holes longer than a day and for coins that stop trading mid-window (3.2 and 3.4 of
  `data_use.md`) are not applied here; they belong with step 4's draw (part 3). Listed in the card's Open.

## Fix of 2026-11-27 (found by shard 3)
The register's 35 `paying_rerun_run` books have no `03_test_plan/paying_rerun_run/`: that run reran other runs' plans
(steps 4 and 6 only), so `--register` stopped on them. **Rule (designer):** a book's plan and `measure.py` are each
found by the plan id in its own run first; else in the one other run whose plan's config equals the book's record
config; none or several: refused with a message naming them, and the shard goes on to the next book. 3 tests (own
run first; the one other run, measure.py from the book's run or else the matched run; none, several, no record
config). On the 120 books: 85 in their own run, 32 in another run, **3 refused** (002-01.b1 more-coins 1h, 010-03.e1
1d, 013-01.d2.d2.b1 1d: the same config in `hold2_rerun_run` and `hold_paying_run`). The result file gains `measure`.

**Refinement (designer, 2026-11-27):** several matches whose plan files and `measure.py` are byte-identical are one plan:
the first in sorted order is used, and the result records every match (`plan_found_in`). Only matches that differ are
refused. 1 test. Now all 120 books resolve: 85 in their own run, 32 in one other run, 3 in two identical runs (the 3
above, `hold2_rerun_run` used; shards 4, 4 and 6).
