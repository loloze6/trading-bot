---
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4094 USD
---
## Findings
- **F1:** Over three days, large rises keep rising rather than giving back. On the 18-bar grid, the top quintile of the past 3-day return in usual moves (mean +2.2) is followed by an unusual 18-bar move of +0.98 % (t 3.29, 1030 cases). The middle quintiles are followed by -0.35 % to -0.54 %. The top quintile minus the middle ones is positive in 7 of 8 years (+0.9 % to +2.2 %; only 2022 is -0.34 %), and the slope is positive in 5 of 6 coins.
- **F2:** That continuation lives above the 30-day average. Above the 180-bar SMA, the top quintile of the 3-day return is followed by +1.36 % (t 2.80, 502 cases), and the bottom quintile by +0.66 % (t 1.89). Below the SMA, the top quintile is followed by -0.15 % (t -0.48, 528 cases). So the tested short on relief rallies stands on the only side where up-runs do not continue, and it gains little there: forecast-active grid cells show -0.17 % (1352 cases) against +0.05 % on flat ones.
- **F3:** The book earns nothing over the coin's 3-day rise. It is short 59 % of bars with a mean allocation of -0.80, and its mean gain per bar is -0.0026 %. Its mean daily return is -0.0106 % against coins that rose in most windows, for example w11 book -0.30 %/day against coin +1.26 %/day, and w21 -0.23 % against +0.57 %.
- **F4:** A recent volatility expansion is followed by rises. The ratio of the 1-day to the 30-day standard deviation of 4h returns, by quintile, is followed by unusual 18-bar moves of -0.73 % (t -2.99), -0.15 %, -0.11 %, +0.39 % and +0.49 % (t 1.71), about 1030 cases each. Top minus bottom is +1.1 % to +2.3 % in 5 of 6 coins; XMR is the exception at -0.10 %.
- **F5:** The 4h bar opening at 20:00 UTC rises by +0.099 % on average (t 6.65, 17517 bars), and the bar opening at 00:00 falls by -0.049 % (t -3.20). The 20:00 bar is positive in all 6 coins (t against the other hours 1.5 to 3.1) and in all 8 years. It stands out across the many angles looked at but carries no graded situation.
- **F6:** Saturday bars rise more than other days: +0.079 % per bar (t 5.68). Saturday minus the other days is positive in all 6 coins and in 7 of 8 years (2023: -0.026 %). It is calendar-only, not graded.
- **F7:** One-day falls bounce. The bottom quintile of the 1-day return in usual moves (mean -1.98) is followed by +0.79 % over 18 bars (t 2.90, 1030 cases), while the top quintile is followed by only +0.17 % (t 0.61). This is weaker evidence given the number of angles examined.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends.g1_up-run-continuation-above-average` (from F1, F2, F3): After a coin's 3-day rise that is large against its usual 4-hour move over the past 30 days, while its price is above its 30-day average, the coin keeps rising over the next three days. The larger the 3-day rise in usual moves, and the further the price stands above its 30-day average, the larger the further rise.
- `024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends.g2_volatility-expansion-precedes-rise` (from F4): When a coin's 4-hour moves over the past day are large against its 4-hour moves over the past 30 days, the coin rises more than usual over the next three days. The larger that ratio, the larger the rise.
- `024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends.g3_one-day-fall-rebound` (from F7, F1): After a coin's 1-day fall that is large against its usual 4-hour move over the past 30 days, the coin rises more than usual over the next three days. The larger the fall in usual moves, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
