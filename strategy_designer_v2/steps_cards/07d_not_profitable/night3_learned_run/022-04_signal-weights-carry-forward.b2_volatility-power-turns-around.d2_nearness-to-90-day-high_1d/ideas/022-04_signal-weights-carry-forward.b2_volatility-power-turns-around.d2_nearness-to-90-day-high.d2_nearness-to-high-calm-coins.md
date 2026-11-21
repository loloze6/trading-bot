---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days, and the more so the lower the coin's volatility over the past 30 days.
Consequence: Weight a long on nearness to the 90-day high most heavily in a coin's calm periods and least in its most volatile ones.
Why:
- F2: The idea's effect sits only near the high. Over 3419 grid cases split by forecast quintile, the 5-day move above drift is +1.24 % in the top quintile (forecast +4.2), against -0.14 % in the bottom quintile (forecast -4.8), -0.60 % in the second and -0.42 % in the middle, so a close far below its 90-day high is not followed by a lower return.
- F5: The slope is weaker in the coins' high-volatility tercile (t 0.53) than in the low and middle terciles (t 1.43 and 1.51), and weaker after a 30-day rise (t 0.45, 1324 cases) than after a 30-day fall (t 1.41, 2095 cases).
- F6: Cost is not the cause: the unusual move per case is +1.52 % over 5 days, 7.9 times the 0.19 % cost of a round trip, at 0.078 trades per day.
