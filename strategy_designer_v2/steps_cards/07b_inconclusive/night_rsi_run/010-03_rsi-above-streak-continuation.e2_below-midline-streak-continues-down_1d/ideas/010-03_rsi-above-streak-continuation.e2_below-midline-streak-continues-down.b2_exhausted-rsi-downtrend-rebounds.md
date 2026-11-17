---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
line: 7.b inconclusive
backtest: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The more days a coin's 14-day RSI has stayed below 50 without a break, counted in days up to the close, the higher its return over the next 7 days, only once the stretch has lasted longer than about four weeks.
Consequence: A very long, unbroken stretch of seller control is a reason to cover shorts rather than add to them for the following week.
Why:
- F1: The tested slope runs against the idea: on the 406 pooled 7-day grid cases with forecast < 0 (BTC and ETH only, since BNB did not run), the excess 7-day return rises with the length of the below-50 run (slope +0.00042 per day, t +1.15), and it also rises on log length (t +0.68), so the result is not a "right side but too small" one.
- F3: That weakness sits in fresh stretches and fades or reverses in old ones: excess 7-day return is -0.0223 for runs of 1–3 days (t -2.48, n 92), -0.0143 for 4–7 days (n 52), +0.0007 for 8–14 days (n 72), -0.0204 for 15–28 days (n 71) and +0.0214 for runs over 28 days (t +1.19, n 43); this ending reversal is what turns the tested slope positive.
