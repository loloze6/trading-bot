---
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
idea tested: N4-01_breakout-drift-lasts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3249 USD
---
## Findings
- **F1:** The book's Calmar of 0.44 fails because of long, deep falls while it stays long: the book was long on 73% of coin-bars. Its deepest fall reached -82.5%, measured over the windows run end to end. In w14 the book lost 68.9% with every coin down 41% to 84%. In w7 it lost 43.9% and in w9 47.1%, with five or six of the six coins losing.
- **F2:** Held days whose close is below the 20-day mean earn nothing, while days well above it carry the gain. The two lowest quintiles of held coin-days by close/MA20 have next-day book returns of -0.0005 (t -0.48, n 2254) and -0.0005 (t -0.58, n 2254). The two highest quintiles have +0.0039 (t 2.97, n 2254) and +0.0070 (t 3.25, n 2254). These are pooled coin-days, not the book's daily mean over coins.
- **F3:** The drift lives only next to the high. On non-overlapping 10-bar samples of held bars, the excess return over the coin's all-window mean is +0.035 (t 2.73, n 266) when the close is within about 1.9% of its 20-day high. In the three quartiles further below the high it is -0.006 to -0.010 (t -0.73 to -1.19, n 266 to 267 each).
- **F4:** Held days with a falling 50-day average carry almost none of the book's gain. These 3695 held coin-days have a mean next-day book return of 0.0001 and contribute 0.08 of summed per-coin book return. The 5456 held days with a rising 50-day average have a mean of 0.0042 and contribute 3.84. This split is pooled coin-days, not the book's daily mean over coins.
- **F5:** The book's gain comes from a few long trades, and the many short ones lose (trades summed per trade, not book days). Of 3269 long trades, the median net return is -2.5% and 41% win. The 722 trades of 7 days or less average -4.85%, and those of 7 to 19 days average about -3.5%. The 620 trades longer than 29 days average +32.7%.
- **F6:** Entries made with the close below the 50-day average lose. These trades average -5.7% (median -7.4%, 27.5% winners, n 305), against +3.0% to +6.4% for the other quintiles.

## Ideas
- `N4-01_breakout-drift-lasts.d1_drift-only-near-high` (from F2, F3, F1): After a coin's new 20-day closing high, its excess rise over the following days appears only while its close stays within a small distance of that high and above its 20-day average. Once the close falls below its 20-day average, the coin's following returns are at or below its average.
- `N4-01_breakout-drift-lasts.d2_breakouts-need-rising-trend` (from F4, F6, F1): The rise after a new 20-day closing high is larger when the coin's 50-day average is rising at that bar's close than when it is falling.
- `N4-01_breakout-drift-lasts.d3_highs-under-trend-fail` (from F6, F5, F4): A new 20-day closing high made while the close is still below the coin's 50-day average is followed by returns below the coin's average over the next days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
