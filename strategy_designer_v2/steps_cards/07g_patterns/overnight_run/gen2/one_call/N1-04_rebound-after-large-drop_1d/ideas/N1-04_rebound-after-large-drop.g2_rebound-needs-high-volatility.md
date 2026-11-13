---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.g patterns
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A large one-day drop in a coin is followed by a higher next close more often when the coin's recent volatility is in the upper part of its own history.
Consequence: Take rebound trades after large drops in high-volatility regimes and refuse them when the coin has been quiet.
Why:
- F4: Large drops rebound more in high-volatility regimes. In the top third of the coin's 120-day volatility rank they rose next day 65.1% of the time, mean +1.21% (t 2.27, n 146). In the bottom third they rose 56.5% of the time, with a negative mean of -0.40% (t -1.10, n 168).
- F6: The large-drop rebound has faded. Next-day hit after large drops was 62.5–67.0% in each year 2018–2023, but only 50.0% in 2024 (t 0.04, n 130) and 53.7% in 2025 (t 0.74, n 136).
