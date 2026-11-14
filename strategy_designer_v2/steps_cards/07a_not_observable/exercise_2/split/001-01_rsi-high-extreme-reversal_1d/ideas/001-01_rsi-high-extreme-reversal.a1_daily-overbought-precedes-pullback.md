---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: 2018 to 2024
---
Idea: On each of BTC, ETH and BNB, after a daily bar closes with its 14-day RSI at a true high extreme (the overbought zone, not merely high relative to recent weeks), the coin's return over the next 5 daily bars is below its own average 5-day return. Observed over several years so that enough separate overbought episodes per coin occur.
Consequence: A trader would refuse new longs, or lean short, for about a week after a coin closes a day deeply overbought.
Why:
- F1: The test ran on BTCUSD only, in one window (w1, 2022) of 120 daily bars, while the plan's data line names BTC, ETH and BNB; it found 3 non-overlapping extreme cases against a minimum of 30, all from 1 coin, so the "2 of 3 coins" rule could never be met.
- F3: The window never held a real high RSI extreme: RSI(14) peaked at 58.0 and had 0 bars at or above 60 or 70, against 79 bars in the 40–50 range. The 15 bars with forecast ≤ −10 had RSI between 54.0 and 58.0 (mean 55.6), so the test's "extreme" came from standardising over 60 bars in a falling market (BTC −21 % over the window), not from high RSI.
- F7: Across all 15 extreme bars, the mean excess return was −2.3 % with a std of 5.7 %; at that spread, about 25 independent cases would be needed to reach t = −2.
- F8: Forward return falls steadily with RSI band: −3.4 % (n 10) at RSI 55–60, −1.0 % (n 20) at 52–55, +0.0 % (n 51) at 45–50 and +1.9 % (n 25) at 30–45, all with std of 4–8 %. The direction matches reversal, but the data never reached the RSI ≥ 70 zone the idea is about.
- F9: The observed rate was about 3 non-overlapping cases per 120 daily bars, and that was with extremes defined relative to the window rather than by absolute RSI. At that rate, 30 cases need about 1,200 coin-days, for example roughly 400 daily bars for each of the 3 coins. The run covered 120 coin-days, about a tenth of that.
