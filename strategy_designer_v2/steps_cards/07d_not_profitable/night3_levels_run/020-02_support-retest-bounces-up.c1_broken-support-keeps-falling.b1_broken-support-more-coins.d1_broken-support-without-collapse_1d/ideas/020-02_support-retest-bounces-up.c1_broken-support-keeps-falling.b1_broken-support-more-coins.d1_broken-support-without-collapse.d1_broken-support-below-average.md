---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin's daily close is below its average close of the past 50 days.
Consequence: A broken support is a reason to be short for about ten days only in a coin already trading under its 50-day average, never in one still above it.
Why:
- F1: The book loses because it is short most of the time in coins that rise. It is short on 78 % of bars. Its gain from the market's own rise is -31.3, against +11.6 from timing, for a net -19.7 (summed daily position gains). It loses in the windows where the coins rose, for example w21 (book -8.3, coins +15.3), w6 (-9.2, +12.9) and w11 (-5.9, +22.7), and earns where they fell, for example w2 (+5.6, -5.9).
- F2: The idea is real but smaller than the coins' drift, so a short on it loses before any cost. Over 2251 grid cases the total 10-day move on the short side is -0.26 % (t -0.86, 50.7 % winners). The verdict's own figures agree: unusual move +0.48 %, against a normal drift of -1.38 % in the short's direction. A round trip costs 0.22 %.
- F4: The coin's trend splits the cases the same way. Cases with the close below its 50-day average gain +0.43 % on the short side (unusual +1.8 %, 895 cases). Cases above that average lose -1.23 % (unusual +0.2 %, 320 cases).
- F5: The 90-day trend shows the same split. Cases whose 90-day return is between -20 % and -8 % gain +3.8 % on the short side (t 3.8, 97 cases), while across all bars the coins with the highest 90-day return rise +6.3 % over the next 10 days.
