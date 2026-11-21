---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, the more it rises over the next 1 day, and the higher its 50-day return the larger that rise. The larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its 50-day return is negative, and the more negative that return the larger the give-back.
Consequence: A trader should buy outsized vol-scaled down days for one day, mostly in coins that are up over 50 days, and fade outsized up days only in coins that are down over 50 days.
Why:
- F2: The short side carries the loss. Short bars earn -2.81 bps a day before fees (n 2958), and -3.51 bps of that is the position's share of the coins' own rise. Long bars earn +7.69 bps a day before fees (n 2823).
- F3: The short side loses most when the coin's 50-day return is positive. There, short bars earn -7.40 bps a day before fees (n 995) and long bars +12.24 bps (n 849). When the 50-day return is negative, short bars earn +6.09 bps (n 710).
- F4: The one-day rebound is concentrated in the largest falls and is larger when the coin's 50-day return is positive. After falls beyond 1.5 usual moves, the next-day excess is +0.71 % with t 1.86 (83 cases) when the 50-day return is positive, and +0.29 % with t 0.57 (127 cases) when it is negative.
- F5: The give-back after rises appears mainly when the coin's 50-day return is negative. After rises beyond 1.5 usual moves, the next-day excess is -0.78 % with t -1.47 (85 cases) when the 50-day return is negative, and only -0.10 % with t -0.35 (165 cases) when it is positive.
- F7: Holding the rebound longer does not help. After falls beyond one usual move, the excess return is +0.32 % over 1 day, +0.15 % over 2 days, +0.07 % over 3 days and -0.16 % over 5 days.
