---
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
idea tested: 001-01_rsi-high-extreme-reversal
step 5: not observable
step 6: none
mode: analyst then deducer
explorations: 2
cost: 0.3192 USD
---
## Findings
- **F1:** The test ran on BTCUSD only, in one window (w1, 2022) of 120 daily bars, while the plan's data line names BTC, ETH and BNB; it found 3 non-overlapping extreme cases against a minimum of 30, all from 1 coin, so the "2 of 3 coins" rule could never be met.
- **F2:** The forecast was 0 on the first 34 of 120 bars: no bar before 34 had RSI above 50, and the forecast needs at least 20 bars of history before it can be standardised. Only 39 bars (33 %) had any short forecast, and 81 bars had a forecast of exactly 0.
- **F3:** The window never held a real high RSI extreme: RSI(14) peaked at 58.0 and had 0 bars at or above 60 or 70, against 79 bars in the 40–50 range. The 15 bars with forecast ≤ −10 had RSI between 54.0 and 58.0 (mean 55.6), so the test's "extreme" came from standardising over 60 bars in a falling market (BTC −21 % over the window), not from high RSI.
- **F4:** The 15 extreme bars fell in only 3 episodes, of 2, 1 and 12 bars. Sampling every 5th bar therefore yields only 2–4 cases whichever grid offset is used, and the episode count, not the grid, sets the limit.
- **F5:** Case-to-case outcomes are noisy and depend on where the 5-bar grid starts. The 5-bar forward return has a std of 7.3 %, and the mean excess return across the five grid offsets ranges from −6.8 % (t −1.84, n 3) to −0.2 % (t −0.10, n 3).
- **F6:** The episode outcomes disagree in sign: excess 5-bar returns from the episode starts were −4.1 % and −13.3 % for the two short episodes and +8.3 % for the 12-bar episode, which reached the deepest forecast (−20).
- **F7:** Across all 15 extreme bars, the mean excess return was −2.3 % with a std of 5.7 %; at that spread, about 25 independent cases would be needed to reach t = −2.
- **F8:** Forward return falls steadily with RSI band: −3.4 % (n 10) at RSI 55–60, −1.0 % (n 20) at 52–55, +0.0 % (n 51) at 45–50 and +1.9 % (n 25) at 30–45, all with std of 4–8 %. The direction matches reversal, but the data never reached the RSI ≥ 70 zone the idea is about.
- **F9:** The observed rate was about 3 non-overlapping cases per 120 daily bars, and that was with extremes defined relative to the window rather than by absolute RSI. At that rate, 30 cases need about 1,200 coin-days, for example roughly 400 daily bars for each of the 3 coins. The run covered 120 coin-days, about a tenth of that.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_daily-overbought-precedes-pullback` (from F1, F3, F7, F8, F9): On each of BTC, ETH and BNB, after a daily bar closes with its 14-day RSI at a true high extreme (the overbought zone, not merely high relative to recent weeks), the coin's return over the next 5 daily bars is below its own average 5-day return. Observed over several years so that enough separate overbought episodes per coin occur.
- `001-01_rsi-high-extreme-reversal.a2_4-hour-overbought-precedes-pullback` (from F2, F4, F5, F9): On each of BTC, ETH and BNB, after a 4-hour bar closes with its 14-bar RSI at a true high extreme, the coin's return over the next 5 four-hour bars is below its own average 5-bar return. This is the same reversal claim at a bar size where overbought episodes occur many times a year.
- `001-01_rsi-high-extreme-reversal.a3_higher-rsi-weaker-week-ahead` (from F3, F6, F8, F9): On each of BTC, ETH and BNB, the further a daily bar's 14-day RSI closes above its midpoint, the lower the coin's return over the next 5 daily bars, and the drop is steepest when RSI reaches the overbought zone. Observed across multiple years, so that the upper RSI bands, including the extreme one, each hold many cases.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
