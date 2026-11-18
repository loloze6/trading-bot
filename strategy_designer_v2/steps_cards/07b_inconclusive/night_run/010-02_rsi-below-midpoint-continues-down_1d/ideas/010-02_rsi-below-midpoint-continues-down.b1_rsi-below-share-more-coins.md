---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-midpoint-continues-down
line: 7.b inconclusive
backtest: 010-02_rsi-below-midpoint-continues-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 14 days that a coin's 14-day RSI has spent below its midpoint, the larger the coin's fall over the next 7 days.
Consequence: Sustained RSI below the midpoint marks sellers in control, and their persistent order flow, including step-by-step forced exits, carries the downtrend forward.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: a pooled 7-day slope t of 1.82 on 815 non-overlapping cases. Only BTC and ETH ran (BNB is absent), and both coins point the same way without reaching the bar on their own (BTC t 0.90 on 408 cases, ETH t 1.61 on 407 cases), so the test is short of cases rather than wrong in sign.
- F2: The effect is mixed over time and leans on one year. At 7 days the slope t by year is 2.87 in 2025 but between -0.98 and +0.59 in every other year, with 2022 to 2024 all negative. Without 2025 the pooled 7-day t falls to 1.16 on 713 cases, and only 42% of windows have a positive slope.
- F5: The book's timing gain before costs is positive (0.00092 a day), and its Sharpe is 0.82, which beats holding by 0.18. The forecast's direction therefore earns, but its size is small relative to 7-day coin moves of about 11%.
