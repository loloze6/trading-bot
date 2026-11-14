---
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
idea tested: N7-01_drift-only-near-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5190 USD
---
## Findings
- **F1:** The Calmar failure comes from one fall: the book's deepest drawdown is -67.5%, running 1,160 days from w1 to its trough in w10. Over those 1,162 days the book's mean daily return was -0.00075, against +0.00297 over the remaining 1,736 days. No other fall is deeper than -43.7% (w11 to w13).
- **F2:** In w1–w10, active coin-days whose 50-day average had fallen over the prior 10 bars lost on average (-0.0013 per day, 503 days, sum -0.65). Active days with a rising 50-day average earned +0.0022 (1,125 days). In w11–w24, both groups earned (+0.0075 on 675 days, +0.0086 on 1,357 days), so the falling-trend days are what carried the early fall.
- **F3:** Measured on the book's daily returns, keeping only the days when the 20-day average had risen over the prior 5 bars lifts Calmar from 0.689 to 0.898. It cuts the deepest fall from -67.5% to -48.4%, keeps the Sharpe (0.99 against 0.96) and keeps most of the mean daily return (0.0013 against 0.0015).
- **F4:** Requiring a rising 50-day average instead cuts the deepest fall further, to -34.4% (or -28.5% with a 10-bar rise above 1.45%), and Calmar reaches 0.78 or 0.85. It costs about half the mean daily return (0.0007–0.0008) and some Sharpe (0.85–0.87).
- **F5:** The book's gain rests on a few long holds while most trades lose after fees. Only 40.6% of 2,830 trades win. Trades held 1 day or less average -4.0% net (526 trades), and those held 1–3 days average -2.8% (634). Trades held 15–40 days average +27.3% (392), and those held over 40 days +183% (27). The median net trade is negative in every quintile of the 50-day slope at entry.
- **F6:** The edge fades when the trend is already stretched; these figures are mean per-coin book returns on active days, not the book's daily return.

## Ideas
- `N7-01_drift-only-near-high.d1_near-high-drift-rising-average` (from F1, F3): After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, only while the 20-day average itself has risen over the last few bars.
- `N7-01_drift-only-near-high.d2_near-high-drift-rising-slow-trend` (from F1, F2, F4): After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, only while its 50-day average has been rising over the last ten bars.
- `N7-01_drift-only-near-high.d3_near-high-drift-not-overextended` (from F6): After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, except when the coin has already risen by a very large amount over the prior 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
