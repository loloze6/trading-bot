---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 5 days, the more so the larger its 10-day return.
Consequence: A trader should size a breakout long by both the distance beyond the 90-day high and the strength of the past ten days' rise, keeping the biggest positions for breakouts that come with a strong run-up.
Why:
- F2: The move fades quickly after entry: the drift-adjusted next-day return in position is +1.13 % in the first 3 days held (308 bars, t 2.79), +0.33 % on days 4 to 10 (714, t 1.40), and -0.04 % on days 11 to 20 (997, t -0.18), so the 20-day hold spreads a short move over many idle days and pulls the mean daily return down to 0.024 % against the 0.05 % required.
- F5: In position, the size of the next day's drift-adjusted gain grows with the distance above the 90-day high: -0.10 % at 5 to 10 % below it (601 bars), +0.04 % at 0 to 5 % below (857), +0.39 % at 0 to 5 % above (382, t 1.70), and +0.95 % at 5 to 15 % above (157, t 1.49); the same order holds on all bars (+0.11 %, +0.22 %, +0.86 %).
- F6: In position, the next day's drift-adjusted gain also grows with the coin's own 10-day return: -0.14 % in the second-lowest quintile, +0.20 % in the middle, +0.35 % (t 2.20) and +0.38 % in the two highest; the 20-day-return quartiles go the same way (+0.09 %, +0.26 %, +0.33 %, +0.35 %).
