# Build: the earlier ideas' sides (next steps B13 and A12; the operator's go, 2026-11-28)
Branch `build-idea-sides`, from `ccr-6624e33e-aakrpv`. Nothing in `trading-bot/` changed. No backtest, no price data.

## Purpose and expected outcomes (written before the run)
**Purpose:** B13 took 0 earlier ideas because none has a known side. One pass gives a side to each earlier untested idea
that names a market profile exactly, so a boxed run can take them.
**Expected:** about 420 ideas concerned (the designer's estimate); a model reading of at least 27 of 30 on a sample
read by hand first; a cost under 8 USD; B13 takes more than 0 ideas in the falling and rising boxes.

## What was built
| File | What |
|---|---|
| `common/target_box.md` | "The earlier ideas' sides": the fact, the pass, the file, the reading order (written before the code) |
| `common/earlier_idea_sides.py` (+ `test_earlier_idea_sides.py`) | the pass: `count`, `sample`, `ask` (resumable, `--max-usd` cap, 6 parallel calls). **Why next to `target_box.py`:** the file it writes lives in `common/` and `target_box.idea_side` reads it |
| `common/earlier_idea_sides.json` | 324 records: run, id, profile, side, sentence, model, date, cost. The earlier runs' idea files are not rewritten |
| `common/target_box.py` | `idea_side` reads: own `side:` line, brief's "X only", then the file (by id; `unknown` stays unknown); `in_box` and `box_ideas` pass the id |
| `orchestration/loop/helper/loop.py` | `box_field` passes the idea's id to `in_box` (one argument) |
| `runs/build_idea_sides/` | my own 30 sides (`sample_my_sides.json`, written before any model answer), the 30 texts, the haiku and sonnet answers, `agreement.py`, the box counts before and after |

**The call:** `lib.call`, closed book, a fixed short prompt with no example of any idea; the model is given the idea's
Idea and Consequence lines only (never the "Why", which carries measured numbers). Answer: one word, then the sentence
copied from the idea. Code refuses an answer outside long, short, both, unknown (recorded `unknown`, with a note); it
records `sentence_found_in_idea: false` when the quoted sentence is not in the text (visibility, not a refusal).

## Counts
Ideas written in all runs: 5,226. With a step 5 answer in some run (tested): 1,261. Not exact in profile (none or one word): 3,545.
Untested, exact profile, but a side already known (own `side:` line or brief's "X only"): 96, left out of the pass.
**Concerned: 324** (not 420).

| Profile | Ideas |
|---|---|
| falling agitated | 134 |
| falling calm | 52 |
| rising agitated | 8 |
| rising calm | 34 |
| choppy agitated | 36 |
| choppy calm | 60 |

## The sample (30 ideas, `random.Random(1)`, read by me before any model answer)
| Model | Agreement | Cost |
|---|---|---|
| haiku | **25 of 30** (below 27: not used) | 0.016 USD |
| sonnet | **30 of 30** | 0.166 USD |
The 5 haiku differences: it read "the larger the rise, the larger the fall next day" as long, and one two-way idea as
long. **Model used: sonnet** (the cheapest tried that passed). Opus was not tried: not needed.
My own reading is one reader's; the 30 ideas are in `sample30_texts.txt` for the designer to check.

## The pass
324 asked, 324 answered, 0 `unknown`, 0 refused. **long 136, short 158, both 30.** 12 answers quote a sentence not found
word for word in the idea (a paraphrase): flagged `sentence_found_in_idea: false`, their sides kept.
**Cost: 1.80 USD** for the pass (it includes the 30 sample answers, reused), 0.016 USD more for the haiku sample: **1.82 USD**, under the 8 USD cap.

| Profile | long | short | both |
|---|---|---|---|
| falling agitated | 58 | 72 | 4 |
| falling calm | 8 | 42 | 2 |
| rising agitated | 7 | 1 | 0 |
| rising calm | 30 | 2 | 2 |
| choppy agitated | 11 | 23 | 2 |
| choppy calm | 22 | 18 | 20 |

## B13's counts (`runs/build_idea_sides/box_ideas_after.py`; B13 takes `both` ideas into no box)
"Before" is measured today with the file moved aside, so it counts the 96 ideas whose side was already known.
| Box | Before the pass | After |
|---|---|---|
| falling calm, long | 0 | **8** |
| falling calm, short | 20 | **62** |
| falling agitated, short | 25 | **97** |
| falling agitated, long | 6 | **64** |
| rising agitated, long | 0 | **7** |
| rising agitated, short | 0 | **1** |
| rising calm, short | 0 | **2** |
The "0 each" of the brief did not hold for three boxes: 96 untested exact-profile ideas already had a side (own line or brief).

## Proofs
- Sample agreement: 30 of 30 (sonnet).
- `idea_side`'s order of reading: `test_the_earlier_ideas_sides_file_is_read_third_and_unknown_stays_unknown` (own line, then brief, then file; unknown and a word outside the three stay unknown).
- A run without a box is unchanged: `test_a_run_without_a_box_ignores_the_earlier_ideas_sides_file` (no field, 0 ideas taken, with the file present).
- The cards' tests: 256 passed with `topics/44_review` and `topics/47_review` left out (they need `scipy`, not installed in this container: not run, so `fold_rules_test.csv` was not rewritten). The bot's tests were not run: nothing in `trading-bot/` changed.

## Open
1. The sides are one model's reading, 30 of 30 on 30; the 12 flagged answers and the 30 `both` are the likeliest to be wrong.
2. A "short" idea in a `long only` brief (or the reverse) is taken into the box by its own side; the book it gives may be flat (step 3's side cap, unchanged).
3. Warning kept from B13: falling-market specialists have not held on the 25 coins; these 130 falling ideas are untested, not promising.
4. The file is a snapshot of today's untested ideas; ideas of later runs carry their own `side:` line.
5. `topics/44_review` and `topics/47_review` tests were not run (no scipy here).
