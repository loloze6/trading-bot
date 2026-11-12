---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's short moving average stays above its long one, the coin's price rises more in the later part of that stretch than in its first weeks. The first weeks after the up-cross often see a pullback from a short-lived peak.
Consequence: A trader should hold little or no long position just after an up-cross and build it only once the up-signal has lasted several weeks.
Why:
- F10: In-position days in a newly started signal do poorly. Days 10–30 after the forecast turns on see the coin fall 0.00135 a day, against +0.0030 on days 30–60. This fits a cross that often fires near a short-lived peak before the trend sets in.
- F8: The trades' gains are carried by the long holds. 351 trades held over 50 days average +21.2%. Every shorter bucket loses on average: 25 trades of 0–2 days lose 12.0%, 65 trades of 2–5 days lose 8.6%, 174 trades of 5–15 days lose 9.7% and 473 trades of 15–50 days lose 8.3%. Only 31% of trades win.
- F5: Measured per trade, a larger entry forecast earns less. 530 trades entered at forecast 15–20 average −2.89% before fees. 150 trades entered at forecast 0–5 average +9.15%.
