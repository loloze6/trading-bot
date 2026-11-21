---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 28-day rise, the larger its return over the next 5 days above its normal drift.
Consequence: A strong 4-week rise is a reason to hold the coin long for the next week, and a 4-week fall is no reason to short it.
Why:
- F1: The idea's gain sits in the top fifth of the forecast: the 5-day return above the coin's mean is +1.06 % (t 2.23, 684 cases) after the highest forecast quintile, while the other four quintiles are all at or below zero (-0.14 % to -0.38 %, t between -0.34 and -1.02).
- F2: Momentum works on the rising side only. On 5-day non-overlapping cases, the slope of the demeaned next-5-day return on the volatility-scaled 28-day return is 110 bps per unit with t 3.08 when the 28-day return is positive (1309 cases), and 32 bps with t 0.53 when it is negative (1246 cases); the short bets' signed demeaned return is +0.23 % with t 0.96 (1719 cases).
- F5: The signal outlasts its 5-day horizon but not 20 days: the scaled 28-day return slope has t 2.87 at 5 days (2555 cases), 2.44 at 10 days (1259) and 0.62 at 20 days (539).
