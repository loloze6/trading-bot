---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
line: 7.d not profitable
backtest: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break beyond about four weeks, counted in days up to the close, the higher its return over the next 7 days.
Consequence: A very long unbroken stretch of seller control is a reason to cover shorts or lean long for the following week rather than add to the short.
Why:
- F2: The longest stretches give back what the shorter ones earn. On the 463 active bars with a run above 30 days, the position is at its largest (mean allocation -1.04) and loses 0.0018 per day, a total of -0.83. The 2428 bars with shorter runs gain 0.000446 per day, a total of +1.07 (Welch t of the difference -1.13).
- F3: On the plan's non-overlapping 7-day grid, the excess 7-day return falls as the stretch lengthens and then turns. It is -0.008 (n 93) for runs of 0–3 days, -0.024 (77) for 4–7 days and -0.025 (106) for 15–30 days, but +0.018 (67) once the run passes 30 days, which is why the pooled slope t is +1.15 and not negative.
- F4: The book rests on one window: w2 alone adds +0.99 of position gain and +0.49 of book return, with a mean run of 33 days and a mean allocation of -0.71. With w2 left out, the stretches above 30 days lose -1.36 against +0.62 for the shorter ones, which is why the lowest Sharpe with one window left out is -0.23.
