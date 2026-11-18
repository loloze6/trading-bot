---
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
idea tested: 012-04_flush-depth-retracement-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3677 USD
---
## Findings
- **F1:** On down days, more volume relative to the prior 20 days' mean goes with a larger 3-day excess return: the slope of the excess 3-day return on log volume ratio is +0.0099 (t 3.70, n 2245 non-overlapping cases), while on up days it is -0.0020 (t -0.88, n 2470).
- **F2:** Among clearer falls (bar return of at most -1 usual move), the same slope is steeper: +0.0267 (t 4.16, n 577).
- **F3:** The effect sits in the top volume fifth. Down days in the highest volume-ratio quintile have a mean excess 3-day return of +0.0179 (t 3.76, n 454), while quintiles 0 to 3 lie between -0.0031 and -0.0007.
- **F4:** The rebound after sharp, heavy-volume falls does not need the wick. Falls of at most -1.5 usual moves with volume at least twice its mean earn a mean 3-day excess of +0.0206 without a long lower wick (n 47) and +0.0278 with one (n 35). The same falls on low volume earn +0.0002 (n 171) without a wick and -0.0115 (n 27) with one.
- **F5:** The tested signal is not what carries the rebound. Fall depth on flush bars has a slope of -0.0031 (t -0.75, n 73), and the book's 151 active days average -0.58% (t -1.67) with only 22.5% positive, from about 12 one-day trades per coin.
- **F6:** The volume-on-down-days slope is stronger in later years than earlier: on all days pooled it is +0.0054 (t 2.53) in 2022–25 against +0.0016 (t 0.58) in 2018–21. By coin it is positive in 4 of 6 (ZEC t 2.05; BTC t -0.84, XMR t -0.74), so it is a pooled effect and not one each coin shows strongly.
- **F7:** Thursday and Friday next-day excess returns beat other weekdays (Welch t 5.01, about 4,960 Thu/Fri days against 12,420 others). The gap is positive in all 6 coins (+0.10% to +0.76%) and in both halves (+0.60% vs -0.15% in 2018–21, +0.11% vs -0.07% in 2022–25). It is a calendar condition with no grade, so I propose no idea from it.

## Ideas
- `012-04_flush-depth-retracement-size.g1_down-day-volume-burst-rebound` (from F1, F2, F3, F4, F6): On a day a coin closes lower, the larger that day's volume relative to its mean over the prior 20 days, the larger the coin's rise over the next 3 days. The rebound comes from the volume burst itself, whatever the size of the lower wick.
- `012-04_flush-depth-retracement-size.g2_volume-graded-rebound-after-falls` (from F2, F4, F5): On a day a coin falls by at least its usual daily move, the larger that day's volume relative to its prior 20-day mean, the larger its rise over the next 3 days. On such days the effect is steeper than on down days in general.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
