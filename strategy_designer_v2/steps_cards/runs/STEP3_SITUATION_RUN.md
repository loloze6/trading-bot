# Step 3: the book trades the idea's situation (topic 47, N3; the operator's go 2026-11-23)

## Purpose and expected outcomes (stated before the runs, in the session)
The change: step 3's prompt listed "a threshold or an on/off condition made graded" as an allowed adaptation; ideas
that name when a position exists ("heavy-volume days", "only the deepest falls") were built as a graded score above 0
on ordinary days (26 of night 5's 72 real books that do not pay; phase A, `runs/BOOK_REFLECTS_IDEA_RUN.md`). New rule
(`03_test_plan/helper/system_prompt.md`): the idea's situation is never graded away; when the idea says when a position
exists, the situation is a regime and the forecast inside it is graded; only a threshold on the idea's strength is
made graded. Expected: the five phase-A ideas gated; ideas graded by nature unchanged; an idea already gated stays gated.

## The test: the same 8 ideas, the old prompt (A) and the new one (B)
| Idea | Idea line | A (old prompt) | B (new prompt) |
|---|---|---|---|
| absorbed selling, low close (1d) | "heavy volume ... low close" | no gate | regime: volume >= 1.5 x its 20-day mean |
| extreme surge, low close (1d) | "volume several times usual ... near the low" | no gate | regime: volume >= 2 x, close in the bottom 20 % of the range |
| volatility-scaled fall rebound (1d) | "a day of unusually large fall" | no gate | regime: a fall of at least 2 usual moves |
| four-hour fade of extreme hours (1h) | graded ("the larger ... the larger"); "only the largest" in its consequence only | no gate | no gate |
| deep 2-hour fall rebound (1h) | graded ("after a fall ... at any hour"); "only the deepest" in its consequence only | no gate | no gate |
| control: nearness-power reversal (1d) | graded | no gate | no gate |
| control: range against its norm, both sides (1d) | graded | no gate | no gate |
| control: volatility-graded weekend reversal (1d) | a weekend condition | regime, 3 runs of 3 | regime, 3 runs of 3 (2 of 3 built with the side by the move's sign and the size by the volatility ratio, a different, faithful form) |
The rule reads the idea's statement (its Idea line), not its consequence: the two hourly ideas state a graded relation.
Cost: about 9 USD of model calls (14 step 3 calls; the first calls of a run cost about 0.78 USD each, later ones 0.07-0.13).

## Steps 4 to 6 on the three newly gated plans (`*/step3_situation_run/`)
| Idea | Book | Step 5 | Size per case (t) | In a position | Yearly | Deepest fall | Calmar | Step 6 |
|---|---|---|---|---|---|---|---|---|
| extreme surge | night 5 | confirmed | +0.17 % | 97 % | 21.3 % | 41.7 % | 0.51 | no |
| | phase A (by hand) | inconclusive | +0.30 % | 12 % | 13.7 % | 34.3 % | 0.40 | no |
| | **step 3, new rule** | **confirmed** | **+2.05 % (3.04)** | **1 %** | 5.4 % | **6.4 %** | **0.85** | **pays** |
| volatility-scaled fall | night 5 | confirmed | +0.19 % | 48 % | 15.2 % | 30.2 % | 0.50 | no |
| | phase A | inconclusive | +0.22 % | 6 % | 2.8 % | 25.9 % | 0.11 | no |
| | step 3, new rule | inconclusive | +0.41 % (0.78) | 3 % | 1.7 % | 19.2 % | 0.09 | no |
| absorbed selling | night 5 | confirmed | +0.14 % | 98 % | 24.2 % | 48.1 % | 0.50 | no |
| | phase A | confirmed | +0.30 % | 12 % | 13.7 % | 34.3 % | 0.40 | no |
| | step 3, new rule | confirmed | +0.38 % (2.11) | 18 % | 19.2 % | 33.1 % | 0.58 | no |
**The extreme-surge book on the unseen dates** (`orchestration/unseen_test/step3_situation_run/`): holds on both
periods by the workflow's rule (2016-17: +0.62 % a case, t 0.42, Sharpe 0.46 against holding 3.75; 2026: +1.18 %,
t 0.72, Sharpe 0.51 against 0.10, 30 cases: "not observable"); step 6 does not pass on either. The edge keeps its sign
but is smaller than in-sample and rests on few cases.

## Reading
- The rule does what it says: the three ideas whose statement names their situation are now gated as stated; graded
  ideas and an already-gated idea are unchanged in kind.
- Tested as stated, one idea pays (extreme surge: Calmar 0.85, in a position 1 % of the days, deepest fall 6.4 %), one
  is inconclusive (its night-5 confirmation was of another book), one is confirmed with a better Calmar (0.50 to 0.58).
- Not yet known: how the rule behaves on a whole run (more ideas, more kinds of situation), and whether a book in a
  position 1 % of the days has enough cases to be trusted out of sample.
