---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin's 10-day return is negative.
Consequence: A short under a broken support should be taken after a 10-day decline and refused after a 10-day rise, which is when these shorts lose.
Why:
- F1: The book loses because it is short most of the time in coins that rise. It is short on 78 % of bars. Its gain from the market's own rise is -31.3, against +11.6 from timing, for a net -19.7 (summed daily position gains). It loses in the windows where the coins rose, for example w21 (book -8.3, coins +15.3), w6 (-9.2, +12.9) and w11 (-5.9, +22.7), and earns where they fell, for example w2 (+5.6, -5.9).
- F2: The idea is real but smaller than the coins' drift, so a short on it loses before any cost. Over 2251 grid cases the total 10-day move on the short side is -0.26 % (t -0.86, 50.7 % winners). The verdict's own figures agree: unusual move +0.48 %, against a normal drift of -1.38 % in the short's direction. A round trip costs 0.22 %.
- F3: The short pays only when the coin is already falling, and loses after a rise. Cases after a 10-day fall of 6 % to 13 % gain +1.75 % on the short side (t 2.4, 407 cases). Cases after a 10-day rise above 5.8 % lose -2.12 % (t -2.7, 408 cases).
- F6: The forecast's grading is largely lost. Two thirds of the cases sit at the -20 cap. The third with the weakest forecast loses -1.12 % on the short side (t -2.2, 751 cases), so many shorts are taken where the support signal is faint.
