---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is negative, the larger its one-day rise measured in its usual daily moves, the larger its fall over the next 3 days.
Consequence: A trader would fade one-day rises in any coin down over the past month, whatever its longer trend, and take a larger short the larger the rise.
Why:
- F1: The book barely trades and so barely earns: only 227 of 36768 bars (0.6 %) were active, the book was non-zero on 305 of 2898 days, and its mean daily return is 0.004 % against 0.138 % for holding the coins, so the 0.71 % per-case edge never adds up to a daily return.
- F3: The fade is graded by the size of the rise and shows more clearly over 3 days than over 1. On non-overlapping 3-day stretches of up days with both returns negative, the slope is -1.88 % per usual move (corr -0.155, p 0.0006, 490 cases), against -0.36 % per usual move at 1 day (corr -0.050, p 0.058). For rises of 2 to 3 usual moves, the 3-day move is -4.96 % (t -3.32, 21 cases) against -1.36 % at 1 day.
- F5: A negative 90-day return is not needed. With the 90-day return positive and the 30-day negative, rises of 0 to 1 usual moves are followed by -0.34 % the next day (t -4.26, n 3754). Over 3 days, rises of 1 to 1.5 usual moves are followed by -1.90 % (t -3.98, 234 cases) and rises of 2 to 3 by -2.07 % (t -2.12, 64 cases). Across all up days with a negative 30-day return, the 3-day slope is -1.11 % per usual move (corr -0.085, p 0.0001, 2231 cases).
- F7: At 1 day, the per-case moves of the broader situations (-0.34 % to -0.81 %) are only 1.5 to 3.7 times the 0.22 % cost of a trade. At 3 days, the same situations give -1.4 % to -5.0 %, 6 to 22 times the cost.
