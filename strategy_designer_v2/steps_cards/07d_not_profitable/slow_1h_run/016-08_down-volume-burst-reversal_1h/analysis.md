---
line: 7.d not profitable
backtest: 016-08_down-volume-burst-reversal_1h
idea tested: 016-08_down-volume-burst-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3299 USD
---
## Findings
- **F1:** The book lost on every coin and in every year (mean daily return -0.00075, coin Sharpes from -1.40 on BTC to -0.29 on XMR), while holding the same coins gained 0.0007 to 0.0016 a day. Its gross gain per bar is close to zero (-0.00002 to +0.00003). Fees take 0.00003 to 0.00004 per bar at about 0.96 trades a day, so the gross timing gain is too small to pay for the trading.
- **F2:** The tested situation predicts the wrong direction on average. After a 72-bar fall, the coin's excess 72-bar forward return is -0.0019 (n=2669). After a rise it is +0.0018 (n=2870), Welch t -1.64. Falls continued rather than reversed.
- **F3:** The forecast barely ranks the outcome. The Spearman correlation of forecast with excess forward return is 0.029 in 30-day downtrends (n=1181) and 0.035 in 30-day uptrends (n=854), and the verdict's top-minus-bottom difference is only 0.0033 (Welch t 1.05).
- **F4:** How deep the fall is matters more than how it was made. Inside falls, the deepest-fall quartile per coin had excess forward return +0.0053 (t 1.38, n=669), and the shallowest-fall quartile had -0.0087 (t -3.11, n=667). The book's held days follow the same order: +0.0009 a day in the deepest volatility-scaled fall quintile against -0.0015 and -0.0012 in the two shallowest.
- **F5:** The 30-day trend splits the result. 3-day falls inside a rising 30-day trend were followed by +0.0032 excess (n=854), and falls inside a falling 30-day trend by -0.0041 (t -1.73, n=1181). The book's held days lost -0.00093 a day (Sharpe -0.85, n=5642) in 30-day downtrends against -0.00039 (n=2673) in uptrends.
- **F6:** In 30-day uptrends the rebound is graded by fall depth against the coin's usual 3-day swing. The two deepest quintiles gave +0.011 (t 1.76, n=126) and +0.011 (t 1.77, n=170), stepping down to -0.0063 (n=208) in the shallowest quintile. In 30-day downtrends every quintile was negative (from -0.0014 to -0.0091).
- **F7:** The losses gather in bear years. Excess return after falls was -0.025 in 2018 (n=402) and -0.0068 in 2022 (n=344), against +0.003 to +0.009 in 2019 to 2021 and +0.005 in 2025.

## Ideas
- `016-08_down-volume-burst-reversal.d1_burst-reversal-in-uptrends` (from F2, F3, F5, F7): When a coin has fallen over the past 3 days, only while its 30-day return is positive, the larger the share of that period's volume traded in its few busiest hours, the more of the fall the coin wins back over the next 3 days.
- `016-08_down-volume-burst-reversal.d2_deep-dips-rebound-uptrend` (from F1, F4, F6): While a coin's 30-day return is positive, the larger its 3-day fall measured against its usual 3-day swing over the past 30 days, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
