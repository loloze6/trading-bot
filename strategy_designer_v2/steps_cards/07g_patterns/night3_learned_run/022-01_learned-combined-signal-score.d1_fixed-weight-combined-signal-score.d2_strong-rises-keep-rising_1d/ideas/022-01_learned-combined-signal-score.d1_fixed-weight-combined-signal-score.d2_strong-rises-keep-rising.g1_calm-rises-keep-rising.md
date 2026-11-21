---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is below its usual level, the larger its 28-day rise, the higher its return over the next 5 days. In that calm regime the extra return following its strongest rises is several times what it is after rises of the same rank in volatile periods.
Consequence: Weight long exposure after strong 28-day rises toward calm conditions, and refuse to scale it up after rises made in turbulent conditions.
Why:
- F1: In the top fifth of 28-day rises, the next 5 days run ahead of the coin's mean when its 20-day volatility is below its median: +2.33 %, t 2.48, 164 cases. When volatility is above its median they barely do: +0.48 %, t 0.71, 346 cases. Calm minus volatile is +1.87 %, Welch t 1.61. Calm cases are positive on all 6 coins (+1.1 % to +5.9 %, t 0.4 to 1.7), volatile cases on only 4 of 6.
- F2: The calm-rise effect sits mostly in the later windows: +3.93 % (t 2.54, 81 cases) in w13 to w24 against +0.75 % (t 0.71, 83 cases) in w1 to w12. Scaling the 28-day rise by volatility shows the same split: top fifth minus the rest is +2.45 % (t 2.67) late and −0.60 % (t −0.90) early.
- F3: Dividing the 28-day rise by its 20-day volatility grades the next 5 days only slightly better than the raw rise. Among rises, the Spearman correlation is 0.053 against 0.036 (1309 cases). The top fifth of the scaled rise gives +0.77 % (t 1.45), against +1.08 % (t 1.96) for the raw rise. So the calm effect in F1 is not just a rise measured in units of volatility.
- F4: The top fifth of 28-day rises leads the coin's mean by +1.08 % over 5 days (t 2.23, 510 cases). Over 10 days the lead is +1.26 % (t 1.18, 252 cases), and over 20 days it is gone (0.00 %, t 0.07, 108 cases). The move is done within about 10 days, unlike the outlasting moves of earlier runs.
