# 7.d exercise 3: final rules, refreshed inputs, ideas taken through the workflow (2026-11-14)

**Inputs.** The card's fixed inputs, 002-01 (golden cross) and 002-03 (close above the 200-day average), backtested
again with the current steps (the sizing rule added by step 3's code; steps 4, 5 and 6 rerun). With the sizing alone:
002-01 Sharpe 0.38 to 0.49, Calmar 0.001 to 0.20; 002-03 Sharpe 0.51 to 0.68, now ahead of holding, Calmar 0.14 to 0.39.
Both still not profitable (002-01: gain against holding and Calmar; 002-03: Calmar only).

**7.d, twice on each** (`run_1/`, `run_2/`, 1.48 USD). Every analysis starts from what failed, measures as the workflow
measures, writes its repairs as the tested idea amended in full, marks new ideas. The same main repair in both runs:
002-01, "only while the coin's recent-weeks return is positive"; 002-03, near the recent high and with a recent rise.

**Three repairs taken through steps 3 to 6** (step 3 read 7.d's idea files directly, keeping only the idea's fields):

| Repair | Step 3 | Step 5 | Book, 6 coins | Book, 9 unseen coins (diagnostic) |
|---|---|---|---|---|
| 002-01 run 2 d1: golden cross, only while the recent-weeks return is positive | plan (exact) | inconclusive (t 0.97) | Sharpe 0.85, +0.30 over holding, Calmar 0.72 (was 0.49, -0.08, 0.20) | profitable: Sharpe 1.22, +0.85, Calmar 1.54 (original book: 0.57, +0.16, 0.34) |
| 002-03 run 2 d1: above the average, the more the closer to the recent high | plan (adapted) | inconclusive (t 0.61) | **profitable**: Sharpe 0.95, +0.40, Calmar 0.92 (was 0.68, +0.11, 0.39) | profitable: Sharpe 1.18, +0.82, Calmar 1.42 (original book: 0.91, +0.49, 0.70) |
| 002-03 run 1 d1: only while the distance above the average widens | missing-components (the change of the distance) | | | |

**Reading.** 7.d's repairs are relevant: each moves the measures that failed, on the 6 coins and on 9 coins the
analysis never saw. Their ideas are not confirmed by step 5: the repairs earn by staying out where the falls are, while
step 5 measures a rise in the mean return (the same as N7-01 in the overnight run).

**What the exercise revealed.** The sizing's longer warm-up costs a few windows (XMR 23/24, XRP 22/24): the parked
warm-up defect of the engine now bites. Both fixed inputs fail on their falls; no input exercises 7.d's other branches
(a gain too weak; too few trades).

## Third input: 002-04, a gain that fails (added on the operator's instruction)

002-04 (short below the 200-day average, refreshed with the sizing): it loses (Sharpe -0.43, -1.00 against holding,
Calmar -0.16). 7.d twice (0.63 USD): both runs start from the gain (the short loses on its own trades, not on fees:
the coin keeps rising while the book is short) and both find that shorts deep below the average rebound.

| Repair | Step 3 | Step 5 | Book, 6 coins | Book, 9 unseen coins (diagnostic) |
|---|---|---|---|---|
| run 1 d1: below the average, the coin keeps falling only while the average itself declines | plan (exact) | inconclusive (t -0.37) | Sharpe -0.16, -0.72 against holding, Calmar -0.09 (was -0.43, -1.00, -0.16) | Sharpe -0.43, -0.83, Calmar -0.21 (original book: -0.38, -0.78, -0.19) |
| run 2 d1: ..., except when the close has already fallen sharply and far below its recent high | missing-components (the distance below the recent high, and the speed of that fall) | | | |

**Reading.** On the falls branch (002-01, 002-03) 7.d's repairs hold on coins it never saw. On the gain branch they
move the measures only on the coins it read, and not on unseen coins: the short side fights the coins' upward drift,
and the conditional cut 7.d found there (t 1.93 in one quartile) does not carry over. Two of the five repairs needed a
component the catalogue does not have (the change of the distance to an average; the distance below the recent high).
