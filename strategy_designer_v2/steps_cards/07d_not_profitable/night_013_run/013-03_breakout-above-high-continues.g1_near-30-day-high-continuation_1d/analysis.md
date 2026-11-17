---
line: 7.d not profitable
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
idea tested: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3211 USD
---
## Findings
- **F1:** The book barely holds the coin. Its mean position is +0.009 and its mean absolute position is about 0.14, it is short on 46% of days and flat on 8%. As a result its mean daily return is 0.000077, against 0.00119 for holding, and its daily standard deviation is 0.0079 against 0.049. Only 0.000011 of its gain comes from the market's own rise.
- **F2:** Longs carry the whole gain and shorts lose it back. Summed daily gains are +2.13 on 4,273 long bars (mean 0.000499) and −0.63 on 4,035 short bars (mean −0.000157).
- **F3:** The forecast's information sits only at the top of the distance range. On non-overlapping 10-day samples, the sextile within 4.5% of the 30-day high or above it has an excess 10-day return of +0.031 (282 cases, 56% up). The five lower sextiles are not graded: they range from −0.014 to +0.003. So the negative forecasts below the usual distance short a coin that does not fall in a graded way.
- **F4:** The effect holds only while the coin's 60-day return is positive. There, the slope of excess 10-day return on distance has t = 3.08 (423 independent cases), and the top tercile shows +0.030 excess against −0.029 for the bottom. When the 60-day return is negative, the slope has t = −1.30 (404 cases), and the near-high tercile shows −0.013 excess.
- **F5:** The book's losses concentrate where it bets against a rising coin. Shorts while the 60-day return is positive lose −0.545 summed (mean −0.000274 on 1,993 bars), while longs in that state earn +1.92 (mean 0.000843). Longs while the 60-day return is negative earn only +0.22.
- **F6:** The result is weak across windows. The pooled book's deepest fall is −22.7%, and 12 of the 24 windows lose money, including windows where holding gained +0.33 to +0.47 (w4, w24). This gives a Calmar of 0.106.

## Ideas
- `013-03_breakout-above-high-continues.g1_near-30-day-high-continuation.d1_near-high-continuation-in-uptrends` (from F2, F4, F5): The closer a coin's daily close is to the highest high of its prior 30 days, the larger the coin's return over the next 10 days, and the effect keeps growing for closes that clear that high, only while the coin's own 60-day return is positive.
- `013-03_breakout-above-high-continues.g1_near-30-day-high-continuation.d2_breakout-strength-drives-continuation` (from F1, F3, F2): Among a coin's daily closes within a few percent of the highest high of its prior 30 days or above it, the further the close sits through that high, the larger the coin's return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
