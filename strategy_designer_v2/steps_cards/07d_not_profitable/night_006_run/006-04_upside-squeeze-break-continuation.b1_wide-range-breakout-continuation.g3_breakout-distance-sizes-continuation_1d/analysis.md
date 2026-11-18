---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3612 USD
---
## Findings
- **F1:** The book barely holds the coin, which is why its mean daily return (1.18e-05 against the required 0.0005) and its Calmar (0.056) fail. Mean absolute exposure is 1.15% of the book, the forecast is positive on only 5.5% of bars, the mean allocation is 0.18 when it is, and the market's own rise contributes 1.4e-05 a day with timing at -2e-06.
- **F2:** The plan dropped the 10-day hold, so the book sells as soon as the close slips back under the prior high. 384 of 519 trades last 1.5 days or less and lose -1.67% net each, while the 34 trades held 3.5 to 15 days earn +14.5% to +45.6% net. The median trade loses -0.60% and 44% of trades win.
- **F3:** The 10-day move after a breakout exists but is concentrated on the breakout bar itself. On the non-overlapping grid, a close above the prior 20-day high is followed by +7.4% excess 10-day return (t 2.29, n 51). Grid bars 1 to 10 days after a breakout show only +0.4% (t 0.43, n 209).
- **F4:** The size of the breakout does not grade what follows, so the idea's distance-sized forecast adds nothing. Excess 10-day returns by distance tercile are +7.7%, +6.3% and +8.2% (n 17 each). Against the largest distance of the past 10 days, the slope's t is -0.31 (n 248).
- **F5:** The breakout's continuation lives in coins already rising over 60 days. In that group, breakouts are followed by +9.0% excess 10-day return (t 2.50, n 42), against -0.4% (t -0.06, n 9) when the 60-day return is negative.
- **F6:** Holding beats the book in nearly every window, which is why Sharpe minus holding fails and the leave-one-window-out Sharpe falls to -0.12. The book's Sharpe is 0.10 against holding's 0.55, and in strong windows such as w11 (coin +1.49 summed daily return) the book makes only +0.02.

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.d1_breakout-continuation-in-uptrends` (from F2, F3, F5): The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days, only while the coin's 60-day return is positive, and the higher that 60-day return, the larger the rise.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.d2_trend-ranked-fresh-breakouts` (from F2, F3, F4, F5): On the day a coin closes above the highest high of its prior 20 days, the higher its 60-day return, the further its price rises over the next 10 days, including the days after its close falls back below that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
