---
idea: 001-02_rsi-low-extreme-rebound
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on the hourly close, read as the contrarian pullback score 50 − RSI. It is kept only when RSI is below 50 (long-only) and is 0 when RSI is at or above 50. The score is standardised against the mean absolute value of its own previous 60 bars (target 10, cap 20). It is then passed through a signed power with exponent 2 and pivot 10. So the forecast is 0 at RSI ≥ 50 and small for mild dips. A dip of average depth gives about 10 (100% long). A deep, extreme low reading gives up to the cap of 20 (200% long). The forecast is never negative and grows smoothly with how far RSI sits below 50.
Config: 001-02_rsi-low-extreme-rebound_1h_config.json
Confirm: Take the bars whose forecast is in the top 10% of that coin-window's bars. Keep only the first bar of each cluster, with at least 24 bars between the kept bars, so overlapping returns are counted once. Measure the forward 24-bar close-to-close return after each kept bar, minus the coin-window's mean 24-bar return over all bars (before costs). The idea is confirmed if the pooled mean of this excess return across all 18 coin-windows is positive with t ≥ 2, and it is positive for each of BTC, ETH and BNB. Supporting check: the same excess return after the top-decile bars is larger than after bars with forecast 0 (RSI ≥ 50).
Reject: The idea is rejected if the pooled mean 24-bar excess return after top-decile forecast bars is zero or negative. A t ≤ −2 would also reject it, since it shows continuation instead of rebound. It is also rejected if the excess return is not positive for at least two of the three coins.
Inconclusive: A pooled excess return that is positive but has t < 2. Also, a significant pooled result driven by a single coin while the other two are negative.
Deviation: "After RSI reaches a low extreme" becomes "while RSI is below 50, sized by depth". Mild dips also hold small, damped positions. Extremeness is measured against the last 60 bars' typical reading, not as a fixed RSI level such as 30. Only the long (low-RSI) side of the brief is tested.
