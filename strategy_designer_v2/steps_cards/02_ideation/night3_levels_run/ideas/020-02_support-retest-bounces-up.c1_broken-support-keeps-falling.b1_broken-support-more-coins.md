---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
line: 7.b inconclusive
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie just above the close, the larger the fall.
Consequence: A close just under a support that held several times is a reason to be short or to refuse a long for the next days, because the stops placed under the level drive the move further down.
Why:
- F1: The tested effect is on the predicted side but almost nil. The mean 5-day unusual move in the short direction is +0.12 % per case (t 0.53, 2058 cases), a strength of 0.005 of the coin's usual 10.6 % move. That is a tenth of the about 0.05 that real ideas usually show (F10 of the findings), and 0.6 times the 0.19 % cost of a round trip, so the book could not pay even if the effect were proven (F11).
- F3: The effect is not concentrated in any part of the data that a condition could isolate:
- F4: The grading is weak and not monotone. The plan's supporting check passes (+0.48 % larger half minus smaller half), but the lowest |forecast| quartile is at -0.48 % (t -1.16) and the higher ones only +0.24 % to +0.34 % (t ≤ 1.10). By quartile of the raw cluster count, the means are 0.01 %, -0.17 %, +0.63 % and -0.01 %, with no ordering.
