---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: 2018 to 2024
---
Idea: On each of BTC, ETH and BNB, the further a daily bar's 14-day RSI closes above its midpoint, the lower the coin's return over the next 5 daily bars, and the drop is steepest when RSI reaches the overbought zone. Observed across multiple years, so that the upper RSI bands, including the extreme one, each hold many cases.
Consequence: A trader would scale down long exposure, or scale up a short, as a coin's daily RSI climbs higher above its midpoint.
Why:
- F3: The window never held a real high RSI extreme: RSI(14) peaked at 58.0 and had 0 bars at or above 60 or 70, against 79 bars in the 40–50 range. The 15 bars with forecast ≤ −10 had RSI between 54.0 and 58.0 (mean 55.6), so the test's "extreme" came from standardising over 60 bars in a falling market (BTC −21 % over the window), not from high RSI.
- F6: The episode outcomes disagree in sign: excess 5-bar returns from the episode starts were −4.1 % and −13.3 % for the two short episodes and +8.3 % for the 12-bar episode, which reached the deepest forecast (−20).
- F8: Forward return falls steadily with RSI band: −3.4 % (n 10) at RSI 55–60, −1.0 % (n 20) at 52–55, +0.0 % (n 51) at 45–50 and +1.9 % (n 25) at 30–45, all with std of 4–8 %. The direction matches reversal, but the data never reached the RSI ≥ 70 zone the idea is about.
- F9: The observed rate was about 3 non-overlapping cases per 120 daily bars, and that was with extremes defined relative to the window rather than by absolute RSI. At that rate, 30 cases need about 1,200 coin-days, for example roughly 400 daily bars for each of the 3 coins. The run covered 120 coin-days, about a tenth of that.
