---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up
line: 7.c rejected
backtest: 020-02_support-retest-bounces-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie just above the close, the larger the fall.
Consequence: A close just under a support that held several times is a reason to be short or to refuse a long for the next days, because the stops placed under the level drive the move further down.
Why:
- F1: The idea's own cases fell instead of rising: over 5 days their mean excess return was -0.54 % (t -2.30, 1595 cases), and it was most negative in the top forecast quartile (-1.03 %, t -2.02, 395 cases); the supporting Spearman was -0.017, so more touches went with weaker outcomes, not stronger bounces.
- F2: The fall comes from closes that slipped just below past 90-day swing lows (0 to 3 % under them), and it is graded by how many lows lie there. On the 5-day grid the excess return is +0.22 % with none (t 0.96, n 2645), -0.29 % with one (t -0.72, n 509), -1.24 % with two (t -1.87, n 163) and -2.22 % with three or more (t -2.86, n 102).
- F3: The graded fall shows on the neighbouring horizons too. With three or more lows just above the close, the 3-day excess return is -1.23 % (t -2.58, n 142). With two lows, the 10-day excess return is -3.24 % (t -2.49, n 73).
- F4: The fall is in both halves of the data. With three or more lows just above the close, it is -1.53 % in w1-12 (t -1.60, n 67) and -3.53 % in w13-24 (t -2.69, n 35). With two or more lows, it is negative on all 6 coins (-0.37 % on LTC to -2.53 % on ETH, t -0.28 to -1.86).
- F5: The fall holds whichever way the coin's 20-day return points. With two or more lows just above the close, it is -1.58 % when the 20-day return was negative (t -2.69, n 207) and -1.75 % when it was positive (t -1.81, n 58).
- F7: The fall is large enough to pay only when several lows lie above the close. With two or more lows, a short earns a total of 1.04 % per case over 5 days, about 5.5 times the 0.19 % round trip, with a strength of 0.156. Counting every case with at least one low, it earns 0.15 % per case, below the cost (strength 0.060).
- F8: How close the price sits to each low adds nothing beyond the count of lows. Among cases with at least one low just above the close, a nearness-weighted count has a Spearman of -0.05 with the 5-day excess return.
