---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, with the reversal growing less than in proportion to the move, so that moderate moves reverse more per unit of move than the largest ones.
Consequence: A trader would fade the daily post-settlement hour with a size that rises with the move but flattens for big shocks, instead of concentrating the book on the extremes.
Why:
- F1: The main measure is on the idea's side and clearly so (mean y 0.0576, t 8.41, 12,716 cases). The result is inconclusive only because the convex part fails: the faded return per unit of move is lower in the top third of moves, by −0.0011. On my own recomputation the top third gives 0.296 % per unit (mean 0.51 %, t 7.24, n 5,696) against 0.413 % for the rest (mean 0.19 %, t 4.21, n 11,390).
- F2: The reversal over the next 24 hours grows with the size of the 00:00-bar move, but less than in proportion to it. By size quintile the mean faded return rises from 0.05 % (t 0.67) to 0.23, 0.30, 0.43 and 0.47 % (t 5.06). Per unit of move it falls from about 0.41–0.56 % in q1–q3 to 0.23 % in q5.
- F3: Concave shapes fit the 24-hour return better than convex ones. The slope's t is −8.54 for sign·√|z| (r² 0.0042), −7.84 for z (0.0036) and only −5.15 for z·|z| (0.0016). The plan's exponent-2 sizing therefore puts its weight where the reversal per unit is weakest.
- F4: The very largest moves do not reverse at all. Moves of 2–3 usual hourly moves fade 0.67 % (t 3.80, n 1,016). Moves of 3–4 fade 0.01 % (t 0.04, n 298), and moves above 4 fade −0.12 % (t −0.18, n 66). These capped extreme cases are the ones the convex test leans on.
- F5: The effect belongs to the post-settlement hour, not to every hour. The 24-hour faded return is 0.30 % (t 7.73) after the 00:00 bar. After the other 23 hours it lies between −0.12 % and +0.10 %, with no hour above t 2.63.
- F6: The effect is broad:
