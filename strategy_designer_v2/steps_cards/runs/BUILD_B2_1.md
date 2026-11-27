# Build B2.1: a run has a target box and stays in it (2026-11-27, branch `build-b2-1`)

## Purpose (written before the build)
Next steps B2.1 (the operator's go, 2026-11-27): each run searches where the portfolio lacks strategies. A run gets a
target box (a market profile and a side), chosen by one rule from the profile map or given by the operator; line 7.g
looks there first; the loop tests in the run only the ideas acting in the box.

## Expected outcomes (written before the build)
1. **The rule on today's map:** the designer expects rising agitated (long or short) first: no idea names it exactly,
   and it is the profile with the largest share of market days or close to it. A box with no exact strategy and a
   larger share would come first instead; the table says which.
2. **The filter on night 9's six runs** (each with its run's header box): most of B's, E's and F's tested ideas kept;
   F's left-out share near night 9's reading (17 of 28 outside); some profitable ideas left out (B's four 074 "bounce
   in a falling market fades" were off its choppy box).
3. **A run without `--target-box`:** the same files as before, the allowed differences being times, shas, run ids and
   the order in which parallel lines finish (as `BUILD_A4_JOIN.md`).
4. Both test suites pass.

## The files
| File | What changed | Shared with |
|---|---|---|
| `common/target_box.md` (new) | the definition: the box, the rule, the run's file, which ideas act in it | |
| `common/target_box.py`, `test_target_box.py` (new) | the rule (`choose`), the run's file (`start`, `run_box`), the filter (`in_box`); `python3 common/target_box.py` prints the table | |
| `orchestration/run_brief/helper/run_brief.py`, test, card | `--target-box auto` or a box in words; written after the data use, before step 1 | |
| `orchestration/select_next/helper/select_next.py`, test, card | one branch in the candidates' status: "outside the run's box (<box>)"; nothing in the record or the score | **build-b10** |
| `07g_patterns/helper/line_prompt.md`, card | `{{TARGET_BOX}}` before "Where to look for a discovery" (empty without a box: the prompt as before) | **build-b10** (7.g) |
| `07_common/helper/analyse.py`, `test_analyse.py` | `target_box_note(run)` fills `{{TARGET_BOX}}` (the run read from the plan's folder); the prompt test fills it too | 7.b to 7.d's prompts are not touched (build-b11-b12) |
| `orchestration/loop/card.md` | the run in its box; `target_box.json` in its storage; no code change | |
| `common/README.md`, `common/market_profile.md` | one line each pointing to the new definition | |
| `runs/build_b2_1/` | the proofs' scripts and outputs | |

**Where an idea's profile and side are written:** both before the test, no fix needed. The profile is the idea file's
`profile:` header line (step 2 and the lines write it). The side is the brief's `side:` header line ("long only",
"short only"; none: both), which step 3 itself reads (`make_test_plan.py`, `brief_side`); the plan's `Side:` and
`Profile:` lines are copies written by step 3's code. The filter reads the idea's brief by its header (the run's copy,
else step 1's lists).

## Proof 1: the rule on today's map
| Rank | Box | Strategies naming it exactly | Share of market days | Score = share / (1 + count) |
|---|---|---|---|---|
| 1 | rising agitated, long | 0 | 21.2 % | 0.2123 |
| 2 | rising agitated, short | 0 | 21.2 % | 0.2123 |
| 3 | falling calm, long | 0 | 20.1 % | 0.2010 |
| 4 | choppy calm, long | 0 | 17.0 % | 0.1701 |
| 5 | choppy calm, short | 0 | 17.0 % | 0.1701 |
| 6 | falling calm, short | 1 | 20.1 % | 0.1005 |
| 7 | rising calm, short | 1 | 17.8 % | 0.0889 |
| 8 | choppy agitated, long | 0 | 7.3 % | 0.0735 |
| 9 | choppy agitated, short | 0 | 7.3 % | 0.0735 |
| 10 | rising calm, long | 2 | 17.8 % | 0.0593 |
| 11 | falling agitated, short | 3 | 16.5 % | 0.0413 |
| 12 | falling agitated, long | 11 | 16.5 % | 0.0138 |

**What comes out: rising agitated, long**, as the designer expected. Why: no idea names "rising agitated" exactly (the
map's 10 long and 2 short there come from ideas naming "agitated" or "rising"), and it is the largest profile on the
map's strategies' coins and dates (21.2 %). Its two sides tie (same count, same share): the long side by the order of
the boxes. **The margin is small:** falling calm, long is next (0 exact, 20.1 %). The shares are read from
`orchestration/combine/boxes.csv` (120 strategies, the box reader on their own records) and the reader on the 11 night
9 records not in it: 131 of 131. On the v3 portfolio's common records (the 25 portfolio coins, 2016-2026) the shares
differ (falling calm 23.5 %, rising agitated 20.2 %) and falling calm, long would come first; the rule uses the map's
coins and dates, as asked.

## Proof 2: the filter on night 9's six runs
Each run with its header's box (`NIGHT9_RUN.md`; B to D name a trend only, or both sides: the same test, the words of
the idea's profile and of the box together still one of the six profiles; sides overlapping). Tested ideas: the rows of
`orchestration/run_idea/<run>/table.json`. Script and output: `build_b2_1/filter_night9.py`, `filter_night9.txt`.

| Session | Run | Box (its header) | Tested | Kept | Left out | of which no profile named | Profitable kept | Profitable left out |
|---|---|---|---|---|---|---|---|---|
| A | night9_chopagishort_run | choppy agitated, short | 28 | 22 | 6 | 5 | 0 | 0 |
| B | night9_chopdeep_run | choppy, short | 35 | 14 | 21 | 5 | 0 | 5 |
| C | night9_chopmonth_run | choppy, both | 35 | 27 | 8 | 8 | 0 | 0 |
| D | night9_chopstretch_run | choppy, both | 31 | 29 | 2 | 0 | 0 | 0 |
| E | night9_fallcalmfade_run | falling calm, short | 33 | 23 | 10 | 7 | 5 | 1 |
| F | night9_fallcalmwide_run | falling calm, short | 28 | 5 | 23 | 6 | 0 | 0 |
| all | | | 190 | 120 | 70 | 31 | 5 | 6 |

**190 tested: 120 kept, 70 left out (31 of them name no profile).** F: 23 of 28 left out (17 in another profile, as night
9's reading said, and 6 naming none). The 6 profitable left out:
- B (choppy, short): five 074 "a bounce in a falling market fades" (four "falling", one "falling agitated"): the
  night's best, found off B's box. In a run with a box they would have been briefs' ideas kept for a later run.
- E (falling calm, short): **074-01.b1.d2_run-break-fade-steep-slide**, the one night 9 candidate admitted in portfolio
  v3: its idea names no profile, so it is not in the box. The rule says so (common/target_box.md): an idea naming no
  profile says nothing of where it acts. Noted as open below.

## Proof 3: a run without `--target-box` gives the same files
- **run_idea, then select_next, on a seeded run** (`build_b2_1/run_one.sh`, from `build_a4_join/run_one.sh`: E's
  074-01.b1.g1 in `proofb21_run`, its plan, verdict and step 7 outputs copied, no model call; steps 4 and 6, the chart
  files, the register and the unseen test for real), once with B2.1's code and once with the 4 code files of
  7b7f0e8bbd8 put back. **1118 files on each side, none only on one: 438 byte-identical, 676 identical once times, shas,
  run ids, temporary paths and durations are masked, 4 different** in the ways `BUILD_A4_JOIN.md` allowed: the order
  in which the parallel step 7 lines finished (`journal.jsonl`, `table.json`, `table.md`), one step's seconds (4.5
  against 4.3), and the bot's own log (the order of two lines). `select_next`'s output and run_idea's output:
  identical. The checkout was restored after each side (0 changes left). `build_b2_1/compare_result.txt`.
- **select_next on every named run** (`build_b2_1/select_next_all_runs.py`: B2.1's ranking against 7b7f0e8bbd8's, read
  only): **65 runs, 5456 rows, all identical.**

## Tests
- The cards' suite: **210 passed** (`VENV -m pytest -q strategy_designer_v2/steps_cards`); `topics/47_review/fold_rules_test.csv`
  restored after it. New tests: `common/test_target_box.py` (4: the twelve boxes, the rule's exact count and score and
  its ties, which ideas act in a box, the run's file written once and kept), one in `test_select_next.py` (a run with a
  box lists the others as outside; a brief's side is read), one in `test_run_brief.py` (a box not one of twelve refused
  before any call); `test_analyse.py`'s prompt test fills `{{TARGET_BOX}}`.
- The bot's suite: **1682 passed, 16 skipped, 75 deselected** (`cd trading-bot && VENV -m pytest -q`; nothing in
  `trading-bot/` changed). A first try with `-n 4` (parallel) failed 3 of `test_built_components.py`'s standard checks;
  that file alone, serially: 112 passed. The parallel run is not the suite's way.

## Open (for the designer and the operator)
1. **An idea naming no profile is in no box** (the rule as given). On night 9 that leaves out E's 074-01.b1.d2, the one
   night 9 strategy in portfolio v3, and 31 of the 70 left out. The map's strategies acting in every profile (79 long,
   2 short, 14 both) could never come from a run with a box. Keep, or count such an idea in every box?
2. **The tie between a profile's two sides** (same count, same share: today rising agitated long and short) goes to
   long by the boxes' order. The operator's rule says "ties go to the larger share", which does not separate them: a
   tie-break of my own, to be confirmed.
3. **The margin of the rule today is small:** rising agitated, long 0.2123 against falling calm, long 0.2010. On the v3
   common records (25 coins) falling calm would win. The shares follow the map's own coins and dates, as asked.
4. **The side is the brief's, not the idea's practice:** a brief with no `side:` line allows both, so its ideas pass any
   box side even when their forecast is one-sided (B's 074 fades are short in practice). The realised side is known
   only after the test (`books.json`, `side`).
5. **Not filtered, by design:** the loop's explicit starting idea (the operator's choice) and an idea resumed mid-test.
6. **Untested with a model:** 7.g's prompt with a box (no model call was made; the text is in `analyse.py`,
   `target_box_note`). The first run with `--target-box` is its test.
7. `topics/NEXT_STEPS.md` line B2.1 not updated here (three sessions build at once; left to the designer).
