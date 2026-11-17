---
brief: 010_rsi-midline-regime-direction
source-idea: 010-04_rsi-below-streak-continuation
line: 7.b inconclusive
backtest: 010-04_rsi-below-streak-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 14-day RSI sits below 50 at the close, the lower its return over the next 7 days.
Consequence: A trader would short coins whose RSI is deep below its midpoint for a week, and would stop treating the age of the down run as the signal.
Why:
- F1: The run length itself carries no continuation. At the plan's 14 days the slope of excess return on days below 50 is +0.00105 (t +1.28, 185 grid cases), which is the opposite side to the idea. The longest runs (41–60 days) are followed by +0.047 (n=14), while 1–5-day runs are followed by −0.017 (n=54).
- F2: The positive slope comes from fold C. There the correlation of run length with excess return is +0.38 for both BTC and ETH, against −0.15 to +0.04 in the other folds. Without fold C the 14-day slope turns to −0.00045 (t −0.57, n=134), still far from any bar.
- F3: Which side of 50 RSI sits on matters more than how long it has been there, and it shows at 7 days rather than 14. Over 7 days the below-50 grid bars average −0.0101 excess (t −1.90, n=406) and the above-50 bars +0.0100 (t +1.76, n=409). Over 14 days the gap shrinks to −0.0068 against +0.0063 (t −0.57 and +0.55).
- F4: Over 7 days the RSI level itself is graded across the midpoint. The slope of excess return on 14-day RSI is +0.00053 (t 1.95, n=719). Every bin below 50 averages −0.008 to −0.017, and the bins from 50 to 70 rise from +0.003 to +0.016. Within either side alone the slope is flat (t −0.76 below, +0.25 above).
