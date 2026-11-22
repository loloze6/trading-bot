---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's 3-day rise that is large against its usual 4-hour move over the past 30 days, while its price is above its 30-day average, the coin keeps rising over the next three days. The larger the 3-day rise in usual moves, and the further the price stands above its 30-day average, the larger the further rise.
Consequence: A trader would ride strong 3-day up-runs in coins trading above their 30-day average and refuse to short them as exhausted.
Why:
- F1: Over three days, large rises keep rising rather than giving back. On the 18-bar grid, the top quintile of the past 3-day return in usual moves (mean +2.2) is followed by an unusual 18-bar move of +0.98 % (t 3.29, 1030 cases). The middle quintiles are followed by -0.35 % to -0.54 %. The top quintile minus the middle ones is positive in 7 of 8 years (+0.9 % to +2.2 %; only 2022 is -0.34 %), and the slope is positive in 5 of 6 coins.
- F2: That continuation lives above the 30-day average. Above the 180-bar SMA, the top quintile of the 3-day return is followed by +1.36 % (t 2.80, 502 cases), and the bottom quintile by +0.66 % (t 1.89). Below the SMA, the top quintile is followed by -0.15 % (t -0.48, 528 cases). So the tested short on relief rallies stands on the only side where up-runs do not continue, and it gains little there: forecast-active grid cells show -0.17 % (1352 cases) against +0.05 % on flat ones.
- F3: The book earns nothing over the coin's 3-day rise. It is short 59 % of bars with a mean allocation of -0.80, and its mean gain per bar is -0.0026 %. Its mean daily return is -0.0106 % against coins that rose in most windows, for example w11 book -0.30 %/day against coin +1.26 %/day, and w21 -0.23 % against +0.57 %.
