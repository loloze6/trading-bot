---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
line: 7.b inconclusive
backtest: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The fewer days a coin's 14-day RSI has stayed below 50 without a break, counted in days up to the close, the lower its return over the next 7 days.
Consequence: A fresh drop of RSI below its midpoint is a reason to stay out of or short the coin for the following week, while a long-standing stretch below 50 is not.
Why:
- F1: The tested slope runs against the idea: on the 406 pooled 7-day grid cases with forecast < 0 (BTC and ETH only, since BNB did not run), the excess 7-day return rises with the length of the below-50 run (slope +0.00042 per day, t +1.15), and it also rises on log length (t +0.68), so the result is not a "right side but too small" one.
- F2: The below-50 state as a whole is followed by lower returns: mean excess 7-day return is -0.0101 (t -1.90, n 406), and the below-minus-above difference is -0.0133 at 7 days (Welch t -1.69, 330 vs 389 cases) and -0.0024 at 1 day (t -2.16, 2334 vs 2788 cases).
- F3: That weakness sits in fresh stretches and fades or reverses in old ones: excess 7-day return is -0.0223 for runs of 1–3 days (t -2.48, n 92), -0.0143 for 4–7 days (n 52), +0.0007 for 8–14 days (n 72), -0.0204 for 15–28 days (n 71) and +0.0214 for runs over 28 days (t +1.19, n 43); this ending reversal is what turns the tested slope positive.
- F4: The fresh-versus-old gap holds in both coins and both halves of the windows: runs of 7 days or less against longer runs give -0.0150 vs -0.0031 in BTC (83 and 114 cases), -0.0161 vs -0.0096 in ETH (76 and 133 cases), -0.0124 vs -0.0068 in w1–12, and -0.0185 vs -0.0064 in w13–24.
