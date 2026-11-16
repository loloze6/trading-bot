---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3678 USD
---
## Findings
- **F1:** While the close is at or above its 200-day average, the coin's 10-day past return predicts its excess 10-day forward return better than the tested range position does. The pooled slope t is 4.40, with 761 grid cases. When both enter one regression on 698 cases, past 10-day return keeps t = 2.85 and the 20-day range position falls to t = 0.91.
- **F2:** In the same regime, the trend shows as a steady rise across past 10-day return quintiles, from -0.0226 in the lowest to +0.0263 in the highest (96 to 212 cases each). Below the 200-day average the slope disappears: t = -0.23 on 786 cases.
- **F3:** Scaling the 10-day return by the 20-day volatility strengthens this. In the trending regime the pooled t is 4.62. The slope is positive in all six coins, with t of 3.49 for XRP, 2.15 for ETH and 2.01 for ZEC.
- **F4:** Large one-day falls tend to reverse the next day. Days in the lowest decile of return scaled by 30-day volatility are followed by an excess next-day return of +0.0061, against roughly -0.002 to +0.002 in deciles 3 to 10 (1,436 cases each).
- **F5:** That reversal is graded on down days. The slope of next-day excess return on the scaled fall is negative in all six coins, with t of -4.42 for XMR, -3.12 for XRP and -2.00 for ZEC.
- **F6:** The reversal is stronger below the 200-day average. After the lowest-decile days the next-day excess is +0.0084 below the average (808 cases) and +0.0031 above it (628 cases). On a non-overlapping 3-day grid, the lowest quintile still gains +0.0043 over the next 3 days (943 cases).
- **F7:** The book's long trades are carried by a few large winners. Their mean net return is +6.13% but the median is -1.21% (2,983 trades). Short trades lose, with a mean of -0.25% and a median of -1.78% (2,161 trades). Average allocation in the trending regime is only 0.19.
- **F8:** Weekday effects do not stand out given how many angles were checked. Saturday's excess is significant at t of about 2 in only LTC (2.02) and XMR (2.23), and is negative for BTC.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average` (from F1, F2, F3): While a coin's close is above its 200-day average, the larger its 10-day return measured against its 20-day daily volatility, the larger its rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g2_sharp-drop-rebound-below-average` (from F4, F5, F6): While a coin's close is below its 200-day average, the larger its one-day fall measured against its 30-day daily volatility, the larger its rebound over the next 1 to 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
