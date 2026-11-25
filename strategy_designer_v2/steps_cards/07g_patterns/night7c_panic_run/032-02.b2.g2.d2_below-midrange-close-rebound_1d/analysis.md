---
line: 7.g patterns
backtest: 032-02.b2.g2.d2_below-midrange-close-rebound_1d
idea tested: 032-02.b2.g2.d2_below-midrange-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3591 USD
---
## Findings
- **F1:** The bigger a coin's one-day fall against its own past 30-day daily volatility, the larger its next-day rise above its normal drift. The bottom decile of the standardised one-day return gains +0.93 % (t 2.11, 722 cases on 225 days) and the second decile +0.46 % (t 1.67). Deciles 5 to 9 sit between -0.06 % and -0.38 %. Over all falls, the mean weighted by the fall's size is +0.84 % (t 2.02, 3520 cases, 867 days).
- **F2:** The fall effect points the same way almost everywhere. In the bottom quintile of the standardised one-day return, all 6 coins are positive (+0.38 % to +1.09 %; XMR t 3.29, ZEC t 2.45), all 4 years are positive (+0.05 % to +1.31 %), and 10 of the 12 windows are positive.
- **F3:** The raw one-day return gives the same picture. Its bottom decile gains +0.93 % the next day (t 2.12, 866 cases, 280 days) and its top decile -0.40 % (t -1.16). The size of the move is what matters, more than the scaling by volatility.
- **F4:** The tested close-below-mid-range effect is largely carried by big down days. Among closes in the lowest fifth of the day's range, the excess next-day return is +0.74 % (t 2.07) when the day's standardised return is in its bottom quintile. It is only +0.25 % (t 0.58) and +0.20 % (t 0.41) in the next two quintiles.
- **F5:** The rebound is stronger when 30-day ranges are wide against 90-day ranges, though not clearly. The size-weighted rebound after a fall is +1.96 % (t 1.61, 307 days) in that regime against +0.08 % (t 0.18, 405 days) when ranges are calm.
- **F6:** The rebound fades within a day. Two days after a bottom-decile day, the excess move is +0.48 % (t 0.97), no larger than the one-day move.
- **F7:** The rebound is large next to the cost of a trade. The bottom decile's excess next-day move (+0.93 %) is about 5 times the 0.19 % cost.
- **F8:** No other angle stood out.

## Ideas
- `032-02.b2.g2.d2.g1_large-daily-fall-rebounds` (from F1, F2, F3, F4, F6, F7): The larger a coin's fall over the past 1 day, measured against its typical daily move over the past 30 days, the larger its rise over the next 1 day.
- `032-02.b2.g2.d2.g2_volatile-regime-daily-fall-rebound` (from F1, F4, F5, F7): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the larger its fall over the past 1 day against its typical daily move over the past 30 days, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
