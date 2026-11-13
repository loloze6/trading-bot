---
line: 7.d not profitable
backtest: N1-06_deep-below-average-rebound_1d
idea tested: N1-06_deep-below-average-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3070 USD
---
## Findings
- **F1:** The book is long-only and fees are not what hurts it: 1030 trades earn a mean of +2.13 % before fees against 0.23 % commission, +2.03 % after fees, and 68.8 % of them win before fees.
- **F2:** The losses come from long holds: the 332 trades held over 20 days lose -4.02 % before fees, while trades held 0–1.5, 1.5–3, 3–7 and 7–20 days earn +4.91 % (n=116), +3.51 % (n=122), +6.00 % (n=200) and +5.28 % (n=252).
- **F3:** The forecast barely separates outcomes. On non-overlapping 10-bar returns minus each coin's mean, every active bucket from forecast 0 to 10 is negative: -0.73 % (n=386, t=-1.01), -0.97 % (n=168, t=-0.94), -0.80 % (n=69) and -0.51 % (n=99). Only forecast 10–20 is positive, at +2.44 % (n=102, t=1.37).
- **F4:** Bear years drive the result. Active 10-bar excess returns are -3.95 % in 2018 (n=137, t=-2.41), -1.62 % in 2019 (n=136, t=-1.91) and -2.51 % in 2022 (n=191, t=-2.65). They are +4.91 % in 2020 (n=73, t=3.03) and +4.16 % in 2021 (n=66, t=1.76). Meanwhile the book is long on 51 % of bars and so ends level with holding (Sharpe gap -0.016, Calmar 0.23).
- **F5:** The rebound appears only in the volatile state. Active bars with 20-day volatility above its 200-day median earn +0.74 % excess over 10 bars (n=140, t=0.68), while calm active bars lose -0.58 % (n=701, t=-1.07).
- **F6:** A bounce inside the decline does not pay. Active bars with a positive 20-day return lose -1.14 % excess over 10 bars (n=234, t=-1.25), against -0.06 % for those with a negative 20-day return (n=607). Active bars with the close above its 50-day average lose -1.33 % (n=125, t=-1.30).

## Ideas
- `N1-06_deep-below-average-rebound.d1_volatile-capitulation-short-rebound` (from F3, F5, F1): When a coin's close falls to an extreme distance below its 200-day average while its recent daily volatility is above its usual level (a capitulation), its price rises over the next one to two weeks more than its normal drift.
- `N1-06_deep-below-average-rebound.d2_rebound-fades-within-weeks` (from F2, F4): After a coin plunges far below its 200-day average, the rebound comes within the first one to three weeks, and after that the price drifts back down with the prevailing decline.
- `N1-06_deep-below-average-rebound.d3_bear-market-relief-rallies-fade` (from F6, F4): While a coin is below its 200-day average and has rallied over the past 20 days, or its close has climbed back above its 50-day average, its price falls over the following ten days relative to its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
