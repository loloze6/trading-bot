# Build B2.1: a run has a target box and keeps to it (2026-11-27, branch `build-b2-1`)

## Purpose (written before the build)
Next steps B2.1 (the operator's go, 2026-11-27): each run searches where the portfolio lacks strategies. A run gets a
target box (a market profile and a side), chosen by one rule or given by the operator, and the run keeps to it.

**Revised the same day** (the operator's review, relayed by the designer): the shares of market days on the 25
portfolio coins; a tie of a profile's two sides to the side with fewer strategies in the map; **no filter**: "why
couldn't we force the analyst to only give ideas around that box, instead of rejecting wrong output or parking them?"
The box becomes part of the brief's theme, given to every step that writes ideas; an idea outside it is only recorded;
a boxed run's brief must name the box. The first version (a filter in `select_next`, a note for 7.g only) is removed
(commits 14ea63b3a22 and 79f4c5e66b2 keep it).

## Expected outcomes (written before each version)
1. First version: rising agitated first (the designer); a run without a box unchanged; both suites pass.
2. Revision: on the 25 coins, **falling calm, long** first (the designer); without a box, the prompts byte for byte as
   before and the same files; with a box, one note after the brief in step 2's and every line's prompt.

## The files (the revision; relative to `strategy_designer_v2/steps_cards/`)
| File | What changed | Shared with |
|---|---|---|
| `common/target_box.md` | the definition: the three ways to start, the rule, the brief's check, the box in the theme, the field | |
| `common/target_box.py`, `test_target_box.py` | the rule (`choose`, shares from the last portfolio's `boxes.csv`), the run's file (`start`), the note (`theme_note`), the brief's check (`brief_refusal`), the field (`in_box`) | |
| `common/theme.md` | a run's target box is part of the theme | |
| `02_ideation/helper/make_ideas.py`, card | the note after the brief (one line) | |
| `07_common/helper/analyse.py`, card | the note after the brief, for every line 7.a to 7.g (one line and the import) | **build-b11-b12** (it changed analyse.py and 7.c's prompt; my diff is 2 lines, next to the brief) |
| `07g_patterns/card.md` | one paragraph; **`line_prompt.md` back to 7b7f0e8bbd8's** | **build-b10** (7.g's call) |
| `orchestration/select_next/` (helper, test, card) | **back to 7b7f0e8bbd8's: no change** | **build-b10** |
| `07_common/helper/test_analyse.py` | back to 7b7f0e8bbd8's | |
| `orchestration/run_brief/helper/run_brief.py`, test, card | `--target-box`; the brief's check before step 2 | |
| `orchestration/loop/helper/loop.py`, test, card | `in_box` in each turn's line of a boxed run | |
| `common/README.md`, `common/market_profile.md` | one line each | |
| `runs/build_b2_1/` | the proofs' scripts and outputs (the night 9 filter count removed with the filter) | |

## Proof 1: the rule on the 25 portfolio coins
The map's strategies: 131; the shares from portfolio v3 (129 common records: the 25 portfolio coins, 2016-2026).

| Rank | Box | Strategies naming it exactly | Strategies acting in it (the map) | Share of market days | Score = share / (1 + exact) |
|---|---|---|---|---|---|
| 1 | falling calm, long | 0 | 2 | 23.5 % | 0.2349 |
| 2 | rising agitated, short | 0 | 2 | 20.2 % | 0.2025 |
| 3 | rising agitated, long | 0 | 10 | 20.2 % | 0.2025 |
| 4 | choppy calm, long | 0 | 2 | 17.4 % | 0.1741 |
| 5 | choppy calm, short | 0 | 2 | 17.4 % | 0.1741 |
| 6 | falling calm, short | 1 | 11 | 23.5 % | 0.1174 |
| 7 | rising calm, short | 1 | 5 | 15.7 % | 0.0784 |
| 8 | choppy agitated, short | 0 | 0 | 6.4 % | 0.0636 |
| 9 | choppy agitated, long | 0 | 5 | 6.4 % | 0.0636 |
| 10 | rising calm, long | 2 | 9 | 15.7 % | 0.0523 |
| 11 | falling agitated, short | 3 | 11 | 16.8 % | 0.0420 |
| 12 | falling agitated, long | 11 | 16 | 16.8 % | 0.0140 |

**What comes out: falling calm, long**, as the designer said. It is the largest profile on the 25 coins (23.5 % of
days) and no idea names it exactly (the map's 2 long strategies there come from "calm" ideas). Rising agitated is second
on both sides (20.2 %); its tie goes to **short** (2 strategies acting there in the map, against 10 long). Choppy calm's
two sides tie on that count too (2 and 2): the map's order (long first) decides, the only tie left. The map counts match
`PROFILE_MAP.md` box by box (2, 2, 10, 2, 2, 11, 5, 0, 5, 9, 11, 16).

## Proof 2: the prompts with and without a box
`build_b2_1/prompts_with_box.py`: step 2's and line 7.g's prompts captured at the model call (no call made) on night 9
E's 074-01.b1.g1 and brief 074, with 7b7f0e8bbd8's code and with this build's, without a box and with "falling calm, long":
- **Without a box: byte for byte identical** (step 2: 16,111 characters; 7.g: 48,162).
- **With a box: +450 characters, the note after the brief**, in both. Lines 7.a to 7.f build their request with the
  same code as 7.g (`analyse.py`, one `context`), so the note is the same for every line. As it appears:

```
[THE MARKET AND SIDE OF THIS RESEARCH: PART OF THE BRIEF'S THEME]
This research is about one market profile and one side: falling calm markets, long positions. They are part of the brief's theme. Every idea you write keeps to them: its situation is in a falling calm market, and it says so in a `profile: falling calm` line; its position is long only. A pattern off the brief's theme is looked for in falling calm markets, for long positions, only.
```

## Proof 3: a run without a box gives the same files
`build_b2_1/run_one.sh` (from `build_a4_join/run_one.sh`): night 9 E's 074-01.b1.g1 through `run_idea`, then
`select_next`, in a seeded run (`proofb21_run`: its plan, verdict and step 7 outputs copied, so no model call; steps 4
and 6, the chart files, the register and the unseen test for real), once with this build's code and once with the 4
changed code files of 7b7f0e8bbd8 put back (`make_ideas.py`, `analyse.py`, `loop.py`, `run_brief.py`; `select_next.py`
and 7.g's prompt are already 7b7f0e8bbd8's). **1118 files on each side, none only on one: 438 byte-identical, 676
identical once times, shas, run ids, temporary paths and durations are masked, 4 different**, in the ways
`BUILD_A4_JOIN.md` allowed: the order in which the parallel step 7 lines finished (`journal.jsonl`, `table.json`,
`table.md`), one step's seconds (3.5 against 3.4), the bot's own log (the order of its lines). `select_next`'s and
`run_idea`'s outputs: identical. The checkout was restored after each side (0 changes left).
`build_b2_1/compare_result.txt`. The loop is not run there (it would call models); without a box `box_field` adds
nothing to a turn's line (`test_loop.py`).

## Addition 1: step 1 writes a boxed run's brief inside the box (the designer, 2026-11-27, after the revision)
Expected: the operator can launch a boxed run with a theme that says nothing of the box; step 1's prompt without a box
byte for byte as before. Built: `01_brief/helper/make_brief.py` takes `--run` (which `run_brief` passes only for a
boxed run, for its brief and its discoveries' briefs alike), pastes the same note after its request, and accepts a
`profile:` header line; the note now also says a brief has both header lines. Proof (`build_b2_1/prompts_with_box.py`,
`prompts_with_box.txt`): **step 1 without a box byte for byte identical** (93,683 characters), with a box +555, the note
after the request; steps 2 and 7.g likewise (16,111 and 48,634 characters; the note is now 555 characters). Tests:
`01_brief/helper/test_make_brief.py` (new: the profile line accepted), `test_run_brief.py` (`--run` only for a boxed run).

## Addition 2: B13, a boxed run starts from the ideas already written in its box (the operator's yes, 2026-11-27)
The rule, written first in `common/target_box.md` (and the loop's card): before its first turn, a boxed run takes the
untested ideas (no step 5 answer in any run's `table.json`) of every other run whose `profile:` line is the box's
profile word for word and whose brief allows the box's side; copied into the run's step 2 folder with
`taken-from: <run>`, their brief into the run's briefs; ranked by `select_next` unchanged; one `loop.jsonl` line each
(`taken`, `from`) and `taken_from` on their turns.

**Ids: the rule that cannot clash.** An idea keeps its id. Two clashes were possible: (a) `run_brief`'s `ideas_of` found
a brief's ideas by number alone, and brief numbers were shared by parallel sessions (E3), so a taken 060-01_x would have
passed for the run's own brief 060_y's (and step 2 skipped); now a brief's ideas are those with its number **whose header
names it**. Proof: the same ideas as before for all **249 briefs of every run (549 ideas)**
(`build_b2_1/ideas_of_all_runs.py`). (b) the same id in two runs: taken once, from the first run by name; an id already
in the run is not taken. Briefs are found by their full id (`find_brief`, as `run_idea` does).

**On today's files** (`build_b2_1/box_ideas_today.py`; 1,261 ideas have a step 5 answer):

| Box | Ideas taken | From (run: ideas) |
|---|---|---|
| falling calm, long | 52 | night7_panic_run: 7; night7_steadydecline_run: 3; night8_choppyagitated_run: 1; night8_choppycalm_run: 6; night8_fallingagitated_run: 6; night8_fallingcalm_run: 12; night8_risingagitated_run: 1; night8_risingcalm_run: 6; night9_chopdeep_run: 1; night9_chopmonth_run: 2; night9_chopstretch_run: 5; night9_fallcalmwide_run: 2 |
| falling calm, short | 72 | night7_panic_run: 7; night7_steadydecline_run: 3; night8_choppyagitated_run: 1; night8_choppycalm_run: 6; night8_fallingagitated_run: 6; night8_fallingcalm_run: 12; night8_risingagitated_run: 5; night8_risingcalm_run: 6; night9_chopdeep_run: 1; night9_chopmonth_run: 2; night9_chopstretch_run: 5; night9_fallcalmfade_run: 13; night9_fallcalmwide_run: 5 |
| rising agitated, long | 8 | night7_chopreversal_run: 1; night8_fallingcalm_run: 5; topic1q_proof_run: 1; topic1t_check_run: 1 |
| rising agitated, short | 8 | night7_chopreversal_run: 1; night8_fallingcalm_run: 5; topic1q_proof_run: 1; topic1t_check_run: 1 |

Falling calm long: 52 (49 different by text and data: `select_next` lists 3 as duplicates); falling calm short 72 (69);
rising agitated 8 on each side (7), two of them from proof runs (`topic1q_proof_run`, `topic1t_check_run`: "every
other run" includes them). No id too long. The 20 falling calm ideas that cannot go long have a "short only" brief.
A run without a box: `take_box_ideas` does nothing (`test_loop.py`), and the seeded proof above covers `run_idea` and
`select_next`, unchanged.

## Tests
- The cards' suite: **217 passed** after both additions (213 after the revision) (`VENV -m pytest -q strategy_designer_v2/steps_cards`); `topics/47_review/fold_rules_test.csv`
  restored. New or changed: `common/test_target_box.py` (6: the twelve boxes; the rule's exact count, score and the
  tie by the map's count; the note empty without a box; the brief's check; the field; the run's file written once),
  `test_loop.py` (the field, nothing without a box), `test_run_brief.py` (a box not one of twelve refused; a boxed run
  refuses a brief not naming its box, with the reason, before step 2). `select_next`'s and `test_analyse.py` are back to
  7b7f0e8bbd8's.
- The bot's suite: **1682 passed, 16 skipped, 75 deselected** (`cd trading-bot && VENV -m pytest -q`; nothing in
  `trading-bot/` changed).

## Open (for the designer and the operator)
1. **Step 1 writes the box only if its model follows the note:** the header lines are asked for, not added by code; a
   brief without them is refused by `run_brief` before step 2 (its reason given). A discovery's brief written in the
   loop is not checked (the lines' output: visibility only); its ideas' turns carry `in_box`.
2. **Choppy calm's two sides tie on the map's count too** (2 and 2): the map's order decides (long first).
3. **The side in `in_box` and in B13 is the brief's**, not the idea's practice: a brief with no side line lets its ideas
   count on either side.
4. **B13 takes from every other run, proof runs included** (2 of rising agitated's 8). And the warning in next steps:
   falling-market specialists have not held on the 25 coins so far (0 of 17 before night 9, 0 of night 9's 11).
5. **Untested with a model:** the note's effect on what steps 1, 2 and 7 write. The first boxed run's `in_box` count is
   its test.
6. The first version's proofs (the night 9 filter count, `select_next` on 65 runs) are removed with the filter; git keeps
   them (79f4c5e66b2).
7. `topics/NEXT_STEPS.md` lines B2.1 and B13 not updated here (left to the designer).
