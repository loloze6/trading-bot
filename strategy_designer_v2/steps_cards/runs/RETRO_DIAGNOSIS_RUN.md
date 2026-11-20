# Run brief: the book's diagnosis on every past record (2026-11-20, written before the run)

**Purpose (improvement I1 of `topics/30_review/WORKFLOW_REVIEW.md`; topic 34's step 3):** before redesigning any step
around "is this effect large enough to trade", check on the records we already have that the notion tells paying books
from the others. Every backtest record whose bar files are in this container (21 runs, about 250 books, daily and
hourly) gets the diagnosis (`common/book_diagnosis.py`), next to its step 5 verdict and step 6 status. Code only, no model
call, no backtest.

**The readings used:** the move per bet over the horizon once the bot can act, net of the coin's drift, divided by the
round trip the backtest paid (the "edge ratio"); the market's share of the book's gain; the move on the signal's own bar.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| R1. The edge ratio separates | Profitable books have an edge ratio clearly above 1 (most above 2); most non-profitable books below 1 | I1 is supported: "a move worth several round trips" is the notion to put in `common/` and in steps 1, 2, 7 |
| R2. The market's share separates the rest | Among books with an edge ratio above 1, those that fail step 6 have a higher market share | I1 needs a second reading: the edge must come from the idea's timing, not the market |
| R3. Neither separates | Profitable and non-profitable books overlap on both | the readings do not explain step 6; rework the diagnosis before using it |
| R4. Step 5 and the bets disagree | Confirmed ideas whose edge ratio is at or below 0 (their bets lose against the drift) | how often step 5's measure is not the move the book captures (candidate D) |

**Limits known in advance:** books of the same idea appear several times (reruns, holding variants): counted per
record, and the duplicates named. In-sample: these are the folds the ideas were chosen on.
