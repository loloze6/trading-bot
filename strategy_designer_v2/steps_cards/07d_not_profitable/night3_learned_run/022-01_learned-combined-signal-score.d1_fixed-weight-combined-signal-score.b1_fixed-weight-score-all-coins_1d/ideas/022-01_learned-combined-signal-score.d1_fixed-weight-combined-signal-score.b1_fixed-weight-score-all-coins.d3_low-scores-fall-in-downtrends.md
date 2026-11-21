---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's four signals are combined into one score, its return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high and minus its 30-day volatility, each weighted equally in its known direction. The fall after a low score is larger the more negative the coin's own 90-day return.
Consequence: A trader should bet against a coin with a low score only while that coin is in a downtrend of its own, since in rising periods the low scores are followed by smaller rises, not falls.
Why:
- F2: The shorts carry about half the book's time but almost none of its gain. Short bars add 0.000028 of the 0.000322 gross gain per bar, against 0.000293 from long bars. Short trades average +0.10 % net (5081 trades), long trades +7.79 % net (5610 trades).
- F3: Shorts are paid for by falling years and lost in rising ones. Short-bar gain per bar is +0.00044 in 2018 and +0.00042 in 2022, but −0.00053 in 2023 and −0.00042 in 2024, when holding earned +0.32 % and +0.28 % a day. Being short against the coins' rise costs 0.000109 per bar.
- F4: The negative-score cases are not falls in total. Coins still rose +0.36 % over 5 days after them (3523 cases), against +1.15 % after positive scores. Most of what a short captures is the unusual move (−0.40 %), not a decline, so the short side's total move is small next to the 0.22 % round trip.
