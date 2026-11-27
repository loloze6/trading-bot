# Build A4, step 1: the three parts and the six shards joined (2026-11-27)

Designer's session, branch `step1-join` from the working branch at 2cbe19c058; the operator's go (2026-11-27, "Go
for step 1"; next steps, recommended order 1).

## Purpose and expected outcome (written before the proof)
- **Purpose:** one working branch holding the new data use (`common/data_use.md`): part 3 (`build-a4-research`, the
  research coins and windows), part 4 (`build-a4-common`, step 9's common record), part 5 (`build-a4-portfolio`, steps
  10 to 12) and part 6's records (the 6 shards, 118 of the 120 candidates known before night 9), with the joins the
  three build records asked for.
- **Expected:** a run without `data_use.json` (every run so far) gives the same files as before the join, the allowed
  differences named; in data use 2, `run_idea` runs step 4 on the run's data, step 9 after step 6's files, no unseen
  test, step 10 after step 9 (a test); both test suites pass.

## What was joined
| Join | What |
|---|---|
| `build-a4-research` (eaf4e3fd56) | merged; `trading-bot/strategies/strategy_components.py`: both sides' new classes kept (the night's 4 and `ScaledMoveSmallnessComponent`), the catalogue's rows (137 classes), the components step's index and journal lines from both |
| `build-a4-common` (3d06a7796e) | merged, no conflict |
| `build-a4-portfolio` (066b0d0cff) | merged; `test_run_idea.py`: both sides' tests kept |
| `run_idea.py` | one reader of `data_use.json` (`data_use_version`; the second copy and part 3's `coins.data_use` call removed); step 4 gets `--data-use` in version 2; step 9 right after step 6's chart files (part 4); **the unseen test not run in version 2** (its dates lie inside the research windows; step 9 replaces it: `data_use.md`, "What it replaces"); step 10 after step 9 (part 5); a test of the whole order, and of the old order without the file |
| `final_test.py` (step 12) | runs on step 9's runner, `common_record.backtest(..., coins.FINAL)`, as part 5's record asked: one runner and one 90-day rule for steps 9 and 12; its own window function removed, its test moved to the common runner's |
| cards | `run_idea/card.md` (no unseen test in version 2), `combine/card.md` (step 12's records) |
| `common-shard-1` to `-6` | merged, no conflict: 118 common records (116 by the shards, 2 by part 4's build) |
| `orchestration/common_record/INDEX.md` | rebuilt from the 118 records with the helper's own `index_line` (the 2 lines already there came out identical) |

## Proofs
| Proof | Result |
|---|---|
| cards' tests | 204 passed (`topics/47_review/fold_rules_test.csv`, rewritten by the suite, restored: E4) |
| bot's tests (`cd trading-bot`) | 1690 passed, 8 skipped |
| `run_idea` without `data_use.json`, before and after the join | **the same files.** E's 074-01.b1.g1 (night 9) run through `run_idea` twice in a seeded run (`proofjoin_run`: its plan, verdict and step 7 outputs copied, so no model call; steps 4 and 6, the chart files, the similarity check and the unseen test ran for real): once with the joined code, once with the 15 code files of 2cbe19c058 put back. Both: confirmed (+4.26), profitable enough, holds on both unseen periods. **1118 files on each side, none only on one: 438 byte-identical, 676 identical once times, git shas, engine run ids, temporary paths and durations are masked, 4 different** in allowed ways only: the order in which the parallel step 7 lines finished (`journal.jsonl`, `table.json`, `table.md`), one step's minutes (5.9 against 5.8), and the bot's own log `trading-bot/results/trading_bot.log` (the order in which the coins were read). Every bar, trade, metric, verdict, check, chart file, register entry and comparison, and unseen result is identical. The checkout was restored after each run (0 changes left). Scripts and result: `build_a4_join/` |

## Not done, for the next steps
- The step 4, 5 and 6 indexes under each run's `common/` folders are not rebuilt (the shards did not commit them;
  nothing reads them: `update.py` reads the record json and the chart file).
- Night 9's 11 candidates: their common records are running (`common-night9-1`, `-2`); the 2 hourly books wait for
  E12 (`engine-e12`).
- No run in data use 2 has gone through the joined `run_idea` on real data: that is part 7, the watched pilot.
