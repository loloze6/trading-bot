# Topic 45: why the research finds almost only long momentum, and what the workflow misses

Status: open (investigated 2026-11-22; changes for the operator's go)  
Where: research: step 6's rule (`06_profitability/helper/rule.yaml`), the books judged alone (topic 44), the one-coin rule
(`common/idea_definition.md`), step 7's lines  
Opened: 2026-11-22, the operator: "really surprised that we are struggling to find non-momentum and non-long-only
profitable strategies: investigate ... what the research workflow is missing".

## Question
Is it the market (nothing else pays on these coins), or the workflow (something else pays and the workflow does not keep it)?

## Seen (scripts and numbers in `topics/45_review/`; daily bars, fold years 2018-2025 only, never the unseen or sealed periods)
**A. The market (`facts.py`).** The core 6 coins rise +0.13 % a day on average with daily swings of 4.8 %; holding them
has a Sharpe of 0.53 (0.6 to 0.9 on most of the 19 coins). The market rises even below its 200-day average (+0.08 % a
day, against +0.17 % above). After a fall of more than 2 usual moves the next day averages +1.5 %; after a rise of more
than 2, +0.09 % (the drift). Daily returns reverse slightly (autocorrelation −0.07), weekly ones continue (+0.06). The
market explains 71 % of a coin's daily moves.

**B. Quick strategy families outside the bot (`sim.py`, Kraken's costs per coin, 40 % a year risk sizing):** on 6 and 19
coins, every short-only family loses (Sharpe −0.1 to −1.4); trend long only is the only family that passes step 6's bars.
**Corrected (the operator, 2026-11-22): "costs erase short-term reversal" was wrong.** Per trade, on the core 6 coins:
| Version | Cases | Size of the next day's move | Edge per trade (mean move in the trade's direction) | Edge / round trip (19.3 bps) |
|---|---|---|---|---|
| every day, against the day's move | 17,504 | 322 bps | +14.6 bps | 0.76 |
| after a fall > 2 usual moves (buy) | 430 | 431 bps | +148 bps | 7.7 |
| after a fall > 1 usual move (buy) | 1,927 | 382 bps | +76 bps | 3.9 |
| after a rise > 2 usual moves (sell) | 554 | 439 bps | −19 bps | −1.0 |
Only the crude version (a position against every day's move, changing side on 54 % of days, a full exit and entry each
time) loses to its costs; the reversal after a large fall has an edge 7.7 times its cost; after a large rise it has none
(the drift). **Lesson (the operator, 2026-11-22):** think logically and challenge what I say before closing a
point: "costs erase short-term reversal" came from one crude simulation and was stated as a fact without checking the
edge per trade against the cost (the workflow's own measure, the size of an idea, `common/measures.md`).

**C. Where the short side pays (`diag.py`):** in the two falling years only (2018: Sharpe 0.73; 2022: 0.32 to 0.70), when
momentum loses (−1.69, −1.39); it loses in the six others. Judged alone over eight years, a short book cannot pass; its
value is as a hedge, which no step judges.

**D. The books step 6 rejected (`rejected.py`, `rejected_books.csv`):** of 285 confirmed ideas, 95 profitable enough;
**50 others failed only on the mean daily return (0.05 % a day) and/or Calmar (0.75)**, with a Sharpe of 0.56 to 1.18,
above holding's. Five of them are unrelated to every paying book and trade both sides (about half their trades short):
| Book | Sharpe | Share explained by the nearest paying book | Momentum (022-03) alone, then with it at equal risk | Failed |
|---|---|---|---|---|
| 026-03.d3 Saturday move continues early week (1h) | 1.08 | 0.05 | 1.04 → 1.42 | mean 0.042 %, Calmar 0.61 |
| 022-04.b1 nearness power turns around (1d) | 0.92 | 0.03 | 1.04 → 1.35 | Calmar 0.54 |
| 016-03 late-evening rebound (1h) | 1.18 | 0.24 | 1.04 → 1.35 | Calmar 0.69 |
| 026-04.b2 heavy weekend moves continue (1h) | 0.89 | 0.07 | 1.04 → 1.26 | mean 0.024 %, Calmar 0.61 |
| 022-04.b2 volatility power turns around (1d) | 0.68 | 0.01 | 1.04 → 1.23 | mean 0.044 %, Calmar 0.26 |
Not yet tested on the unseen dates (the unseen test runs only on profitable books).

## What went wrong in the past runs (2026-11-22, the operator's correction: the idea's verdict was forgotten)
1. **Success is a paying book, not a confirmed idea.** The loop's goal and `select_next`'s record count only an idea
   confirmed and profitable (since 2026-11-19, topic 30). A confirmed idea whose book does not pay counts for nothing:
   190 of 285 confirmed ideas; nothing records them as a result, and only paying books enter the similarity register.
2. **Step 7 turns real ideas into momentum, mostly through ideas of its own** (`topics/45_review`, configs compared,
   2026-11-22). Lines run by the verdict and the check: line 7.d on every book that does not pay, whatever step 5 said;
   its prompt allows a repair (the tested idea amended: "..., only while ...") or "an idea of its own", and nothing
   ties its ideas to the brief's theory. Every child step 3 planned from a confirmed idea, against its parent's config:
   | What the child did with the parent's real idea | 7.d | 7.g | Adding a trend or momentum part | Paid |
   |---|---|---|---|---|
   | kept it whole (a repair) | 8 | 4 | 3 of 12 | 4 of 12 |
   | kept part of it | 1 | 12 | 6 of 13 | 1 of 13 |
   | replaced it (an idea of its own) | 7 | 10 | 14 of 17 | 1 of 17 |
   Example: 022-04.b2 (unrelated to every paying book, share 0.01): its 7.d children "four-week momentum continues" and
   "nearness to 90-day high" replace it. Then the loop tests first the children of the lines whose ideas paid.
   Line 7.d on ideas not confirmed: 100 children planned, 7 confirmed and profitable, all momentum: 6 near copies of
   paying books (0.75 to 0.99 explained) and 025-03.d2 (0.50, the calmer momentum book of `runs/NIGHT4_RUN.md`).
   Limits: 42 children; "a trend or momentum part" is read from the component classes (one of them,
   VolatilityScaledReturn, also serves reversal ideas).
3. **Many confirmed ideas were never followed:** the 50 books rejected only on step 6's mean and Calmar have 31 children
   in all, 18 never tested; three of the five unrelated ones have none (a stopped run's last idea; reruns that run no
   step 7).
4. **Step 6's two bars, on the days the book is in a position** (the operator's proposal; `rejected.py` and the
   reading of 2026-11-22): four of the five unrelated books are in a position on 82 to 100 % of days, so the change is
   small; 026-03.d3 (mean 0.051 %, Calmar 0.76) and 016-03 (0.072 %, 0.76) would pass, 026-04.b2 (on 53 % of days:
   0.024 % to 0.046 %) nearly. The two 022-04 books are always on: their low Calmar (0.54, 0.25) is a real deep fall
   (41 %, 55 %). Mathematically: a day out of the market has a return of 0, so the chained value, its peaks and its
   deepest fall F are unchanged; only the number of days counted falls, from N to s x N (s, the share of days on). The
   yearly return A = G^(365/N) - 1 becomes (1 + A)^(1/s) - 1 (about A / s), so Calmar becomes ((1 + A)^(1/s) - 1) / F,
   and the mean daily return is divided by s exactly. It reads "per year in the market": right when the capital is used
   by other books when this one is off (topic 44), too generous for a book held alone.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. The unseen test on the five unrelated confirmed books (step 4 with the unseen windows, no model call) | whether they hold out of sample | none |
| B. The confirmed idea as a result: confirmed books recorded and compared with the paying books (the similarity check on confirmed books too), reported with each run | the variations the research finds stay visible and can be combined | changes the operator's decision of 2026-11-21 (paying books only) |
| C. Step 6's mean daily return, and Calmar's yearly return, on the days the book is in a position (the operator's proposal) | a selective book judged for what it does when on | 2 of the 5 would pass; Calmar keeps its meaning |
| D. Line 7.d keeps the idea's own effect when it proposes how a book could pay (exit, holding, size, a condition from the idea's own theory), and the loop's record counts a confirmed idea unrelated to the paying books | the research no longer turns real non-momentum ideas into momentum | a change to 7.d's card and to the score |

Recommended: A, then B and C; D after reading A.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-22 | No unseen test on the five unrelated books (option A) | the operator | not the question: what blocks real non-momentum ideas is how the workflow treats them | - |

## Links
`topics/45_review/`, `06_profitability/card.md`, topics 41, 42, 44, `runs/NIGHT4_RUN.md`, `runs/SHORT_1D_RUN.md`.
