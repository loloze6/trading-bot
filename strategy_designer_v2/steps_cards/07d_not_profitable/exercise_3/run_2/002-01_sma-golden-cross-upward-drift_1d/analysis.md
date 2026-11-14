---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3441 USD
---
## Findings
- **F1:** The book's daily chain fell 93.1% at its deepest. The fall stayed within 12–27% through w10, deepened to 71% in w13 and reached 93% by w21. Inside w11–w18 the book badly trailed holding: w13 −54.8% against −30.0%, w16 −35.4% against +35.8%, w18 −60.0% against −22.0%. This is what sinks Calmar (0.001).
- **F2:** On the book's worst 2% of active bars (n=200), it held a mean allocation of 1.78, against 0.94 over all active bars. Those bars also had 20-bar volatility of 0.078 against 0.045, and sat 18.4% below the 20-bar high against 10.9%. The largest positions sat in the most violent, already-falling markets.
- **F3:** When the 50/200 spread had risen over the last 10 bars but price had fallen over the last 20 bars, the position lost money. Its mean daily gain was −0.0019, with a Sharpe of −0.51 and summed gain of −2.46 over 1,292 bars. Its non-overlapping 10-bar excess return was −0.0248 (t −1.74, n=116). The same rising spread with price up over 20 bars earned +0.0291 (t 2.07, n=239), with a daily Sharpe of 1.06.
- **F4:** Forecast size bought risk rather than edge. Allocation rose to 1.87 on average in the top forecast bucket (15–20). There the next-bar return was only 0.00155, against the coins' holding mean of 0.00129, while its standard deviation rose from 0.0486 to 0.0589.
- **F5:** The drift is strongest when the spread is smallest. Active bars in the lowest spread quintile returned 0.00273 per bar (t 2.99). The two highest quintiles returned 0.00084 (t 0.77) and 0.00144 (t 0.93).
- **F6:** The drift is also weak when the spread has already jumped. Active bars in the top quintile of 10-bar spread change returned 0.00048 (t 0.32). The middle quintile returned 0.00281 (t 2.62).
- **F7:** Across the book, active bars returned 0.00074–0.00155 per bar by forecast bucket. That is little above the coins' 0.00129 holding mean, which leaves a Sharpe 0.19 below holding's.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_golden-cross-needs-price-confirmation` (from F1, F2, F3): While the 50-day SMA is above the 200-day SMA, price keeps drifting upward, graded by the spread, only while price itself has been rising over the recent weeks. The more the recent price trend points down while the spread is still widening, the more price falls over the next days.
- `002-01_sma-golden-cross-upward-drift.d2_fresh-cross-beats-extended-trend` (from F4, F5, F6, F7): While the 50-day SMA is above the 200-day SMA, price keeps drifting upward, except that the drift is largest soon after the cross while the spread is still narrow. The drift shrinks as the spread grows wide or jumps sharply.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
