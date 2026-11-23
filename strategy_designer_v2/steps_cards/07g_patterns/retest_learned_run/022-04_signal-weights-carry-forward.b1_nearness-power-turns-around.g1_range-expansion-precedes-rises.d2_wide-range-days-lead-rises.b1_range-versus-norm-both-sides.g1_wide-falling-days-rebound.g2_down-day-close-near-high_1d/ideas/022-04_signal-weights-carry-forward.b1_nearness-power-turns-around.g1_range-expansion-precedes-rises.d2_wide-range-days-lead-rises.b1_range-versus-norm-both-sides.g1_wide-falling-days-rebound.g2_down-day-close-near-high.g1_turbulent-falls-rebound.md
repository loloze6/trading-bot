---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the higher its volatility over the past 10 days relative to its volatility over the past 60 days, the higher its return over the next 3 days above its usual drift.
Consequence: A trader would lean long after a falling day that comes inside a burst of turbulence, more strongly the larger the burst, and refuse longs after falls in quiet stretches.
Why:
- F1: On down days, the coin's 10-day volatility relative to its 60-day volatility predicts its 3-day excess return far better than the tested close location. The rank slope's t is 5.41 over 2245 non-overlapping cases, against 2.65 for close location on the same down days. The excess return rises from −1.147 % in the lowest quintile to +1.803 % in the highest, a spread of about 15 times the 0.19 % cost of a trade.
- F2: This down-day volatility effect is not the short reversal after a large day. Controlling for the day's return scaled by its 30-day volatility leaves its t at 5.20, while that control's t is −0.53 (2245 cases).
- F3: The down-day volatility effect holds at other horizons and in most coins and years. Its t is 5.83 at 1 day (7151 cases) and 3.43 at 7 days (928 cases). The slope is positive in every coin (t 1.27 to 2.78, five of six near or above 2) and in 7 of 8 years (strongest in 2018 at t 4.73; only 2023 at −0.13).
- F6: The tested book sizes up exactly where it earns least. In the top forecast quintile (mean forecast 12.2) the next-day return is −0.010 % and the position's gain is −0.002 %. In the bottom quintile (forecast 1.6) these are +0.448 % and +0.123 %. This fits the book's negative timing gain (−7.9e-5 a day) despite step 5's slope t of 3.07.
