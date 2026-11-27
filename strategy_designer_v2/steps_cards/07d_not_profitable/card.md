# Step card 7.d: Confirmed, not profitable (2026-11-12; entry and proposals changed 2026-11-22)

## Business objective
**Establish why the book of an idea confirmed real does not pay, starting from the measures that failed, and propose repairs: the same idea traded another way so that it pays (`../common/idea_created_from.md`, "A repair of a confirmed idea"), or, rarely, say that none would.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **confirmed**, step 6's check is **not profitable enough** (operator, 2026-11-22), and the book is
**close**: it fails **at most 2** of step 6's 6 measures (`../06_profitability/helper/rule.yaml`; B12, operator
2026-11-27: `step6_failed_at_most: 2`). Otherwise the line does not run, and its index line says so, with the count of
failed measures (`helper/line.yaml`). A strategy that is not close gets no repair: its effect stays recorded
(confirmed) for the combination, and line 7.g still runs on it.

Why close (B12, nights 7 to 9, `../topics/47_review/night9_review.txt` part 4): of 135 repairs, the parent failing 1
measure became profitable 6 times in 28; failing 2, 4 in 56; failing 3 or more, 0 in 51. A repair adds a median of 0.00
to Calmar (one in ten adds 0.34 or more): a repair is tuning, which reaches the bar only from near it. No "large
repair" line (the operator's question, 2026-11-27): 0 of 51 far strategies became profitable. A book whose idea is not confirmed is read by the verdict's line (7.a, 7.b, 7.c) and by 7.g: why the idea is unclear or wrong comes before how its book could pay.

Why (topic 45, measured 2026-11-22): of the ideas line 7.d wrote from books not confirmed, 100 were planned and 7 paid, all momentum (6 near copies of paying books, 0.75 to 0.99 explained, and one half explained). Of the ideas written from confirmed books (lines 7.d and 7.g), those that kept the confirmed idea whole paid 4 times in 12; those that replaced it paid once in 17, and 14 of those 17 added a trend or momentum condition: the observed drift of this line toward momentum.

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
**First, what failed.** The check names the measures that failed; the analysis must explain those.
- The falls failed (the deepest fall against the yearly return): the book's deepest falls, what the coin's bars showed before and during them, what the book held then. The question: when should this book not be in the market?
- The result rests on one period (it fails with one window left out): what that period had that the others did not.
- The gain failed (the gain against its risk, against holding, or its size): where the gain is lost: the forecast's size against what follows, the trades against their fees, the market states that lose.
- It trades too little: what makes the signal rare.

Then the rest, only as far as it explains what failed.

## What it proposes
Repairs that change what failed. An idea that adds gain but leaves the failing measure where it is does not answer.
- A repair keeps the confirmed idea's situation and its signal, in its own words, and changes how the book uses them (`../common/idea_created_from.md`). Written in full ("..., only while ...", "..., except when ...", "..., held for ...").
- A way of trading can become an idea about the market: a stop that would have saved the book says that after a given fall the coin keeps falling; a signal that trades too often says its information is in its slow part.
- **The self-check (operator, 2026-11-22):** a condition the repair adds must not be an effect of its own: if the condition alone could make the book pay, it is a separate idea and is left out. The analyst measures it in its exploration (the bars where the condition holds without the idea's signal, against those where both hold) and gives the measure in the finding, with why the condition belongs to the idea's own theory (a sentence alone was not applied: in the proof's first pass, 3 of 14 repairs added a trend condition and none measured it). Momentum is not named in the prompt (a named effect would bias the analyst against a trend condition the idea's theory calls for); the drift is measured instead: each repair's book against its parent's and against the paying books (the similarity check).
- No separate claim: it would be tested alone and cannot repair this book.
- **No ideas, rarely** (operator, 2026-11-22): only when the analyst shows that the effect itself cannot be traded in any version of the idea (its situation, its strength, its horizon, its side). A weak case is a reason to look for a stronger one: an idea too small with one setting (a reversal after an RSI of 30) may pay with another (after 20). The cost is not named in this sentence: a cost figure invites closing an idea that is only tuned wrongly, and the analyses quoted cost multiples throughout (topic 45). Example of a real effect traded the wrong way: a one-day reversal against every day's move loses, the same reversal after a fall of more than 2 usual moves pays (topic 45).

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
Since 2026-11-22, confirmed books that do not pay (the earlier inputs, 002-01, 002-03 and 002-04 of the full-data run, are inconclusive and no longer enter this line): the set of the proof of 2026-11-22 (`validation/reading.md`).

## Variants compared
One call against analyst then deducer: one call kept, for every line (`../07_common/card.md`).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the measures that failed move the right way, without breaking the others (operator, 2026-11-14). Status: **validated** (operator, 2026-11-14) by exercise 3 (`validation/reading.md`): on the falls, the repairs move the failing measures (002-03's book becomes profitable); the final review's fixes confirmed by a third run. Earlier: exercises 1 and 2 ran; "start from what failed" approved by the operator on 2026-11-13 after the overnight test (overnight test, in git history) (`../07_common/validation/reading.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
