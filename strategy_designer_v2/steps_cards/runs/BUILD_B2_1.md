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

## Tests
- The cards' suite: **213 passed** (`VENV -m pytest -q strategy_designer_v2/steps_cards`); `topics/47_review/fold_rules_test.csv`
  restored. New or changed: `common/test_target_box.py` (6: the twelve boxes; the rule's exact count, score and the
  tie by the map's count; the note empty without a box; the brief's check; the field; the run's file written once),
  `test_loop.py` (the field, nothing without a box), `test_run_brief.py` (a box not one of twelve refused; a boxed run
  refuses a brief not naming its box, with the reason, before step 2). `select_next`'s and `test_analyse.py` are back to
  7b7f0e8bbd8's.
- The bot's suite: **1682 passed, 16 skipped, 75 deselected** (`cd trading-bot && VENV -m pytest -q`; nothing in
  `trading-bot/` changed).

## Open (for the designer and the operator)
1. **Step 1 writes no `profile:` line** (its header keys: venue, instruments, bar, period, side, source). A boxed run
   started from `--theme` or `--source` is therefore refused after step 1's call (about 0.05 USD), the brief kept in
   step 1's list. Today a boxed run starts from a brief file whose header the operator writes. Smallest fix, proposed:
   step 1 gets the same note (the box in its request) and `profile` among its header keys.
2. **A discovery's brief in a boxed run is not checked** (it is the lines' output: visibility only); its ideas' turns
   carry `in_box` like any other.
3. **Choppy calm's two sides tie on the map's count too** (2 and 2): the map's order decides (long first).
4. **The side in `in_box` is the brief's**, not the idea's practice: a brief with "long and short" lets its ideas count
   in on either side.
5. **Untested with a model:** the note's effect on what the lines write. The first boxed run's `in_box` count is its
   test (what share of its ideas keep to the box).
6. The first version's proofs (the night 9 filter count, `select_next` on 65 runs) are removed with the filter; git keeps
   them (79f4c5e66b2).
7. `topics/NEXT_STEPS.md` line B2.1 not updated here (left to the designer).
