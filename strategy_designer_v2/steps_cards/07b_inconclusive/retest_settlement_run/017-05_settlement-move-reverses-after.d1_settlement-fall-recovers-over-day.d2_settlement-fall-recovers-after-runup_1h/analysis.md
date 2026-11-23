---
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2247 USD
---
## Findings
- **F1:** The supporting check could not pass as built, because 61 % of the 5,749 cases sit at the forecast cap of 20 and the median forecast is 20, so the "upper half" (strictly above the median) is empty and the check returned None; the inconclusive status comes from this saturation and not from the effect.
- **F2:** The main measure is on the side the idea predicts (mean 0.00338, t 3.15 on 5,740 cases), and the grading the check was meant to test is there in the uncapped ranks: the lowest forecast quintile (mean forecast 4.8) has an excess 24-hour return of −0.11 % (t −0.86), while the top quintile has +0.40 % (t 2.27).
- **F3:** The effect is graded by the depth of the fall. The deepest quartile of the 2-hour fall against the coin's usual 2-hour move has an excess 24-hour return of +0.57 % (t 3.85, 1,079 cases), against +0.00 % to +0.03 % in the other three quartiles.
- **F4:** The effect is also graded by the run-up. By 7-day return quartile, the excess 24-hour return rises from +0.01 % (t 0.07) to +0.04 %, +0.24 % (t 2.13) and +0.37 % (t 2.07), each on 1,348 cases.
- **F5:** The effect is mixed across settlements, coins and years:
- **F6:** Much of the excess is not tied to the settlement clock. With the same situation (a 2-hour fall and a positive 7-day return) at every hour of the day, the excess 24-hour return is positive at most hours, for example hour 1 at +0.30 % (t 3.46), hour 2 at +0.30 % (t 3.55) and hour 13 at +0.25 % (t 3.06), against 16:00 at +0.26 % (t 3.17). The graded product's t at 16:00 (2.62) is matched at hours 6 (2.80) and 9 (2.59).
- **F7:** The size is small against the cost of a trade. The unusual move is +0.18 % per case (strength 0.035), equal to the 0.19 % cost (1.0 times), and the total move of +0.33 % is 1.7 times the cost. A clear confirmation alone would not make the book pay much more than holding the coin.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins` (from F1, F2, F3, F4): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
