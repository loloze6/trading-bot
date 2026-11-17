---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the coin's 20-day volatility is low or moderate, the larger a down day's volume relative to its 30-day average volume, the larger the coin's rise over the next 3 days.
Consequence: Lean harder into rebounds after heavy-volume down days in calm markets, and refuse them when volatility is already at its highest.
Why:
- F1: On down days of any size, the next 3 days' excess return rises with the day's volume against its 30-day average. Pooled log-volume-ratio slope 0.0129, t 4.05, controlling for the fall's size, whose own coefficient is 0.0003 (t 0.16). Non-overlapping 3-day grid, 2023 cases.
- F7: The volume effect is concentrated where the coin's 20-day volatility is low or middling. On the 3-day grid, the log-volume slope is 0.0066 (t 2.64) and 0.0104 (t 3.35) in the lower two volatility terciles. It is -0.0014 (t -0.35) in the highest tercile, n about 1428 each.
