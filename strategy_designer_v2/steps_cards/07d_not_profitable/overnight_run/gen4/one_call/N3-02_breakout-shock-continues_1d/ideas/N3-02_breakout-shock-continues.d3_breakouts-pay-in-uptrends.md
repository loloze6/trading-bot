---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-02_breakout-shock-continues
line: 7.d not profitable
backtest: N3-02_breakout-shock-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The rise after a new 20-day closing high happens when the coin's close is above its own long average, for example its 200-day mean. When the close is below that average, the new high is followed by a fall over the next ten days.
Consequence: A trader should take new-high breakouts only while the coin trades above its long-term average and refuse them below it.
Why:
- F6: Losses concentrate in falling-market years. 10-bar returns after signals are −5.1% in 2018 (t −1.66, 41 cases) and −2.4% in 2022 (t −1.58, 62 cases). They are +6.2% in 2020, +6.2% in 2021 and +6.1% in 2024 (t 3.57, 2.14 and 2.81). The book's daily return is negative in 2022 and 2023.
- F1: The book's information outlives its holding: 556 new-high signal cases taken at least 10 bars apart rise on average +0.40% over 1 bar (t 1.94), +1.46% over 5 bars (t 3.11) and +2.84% over 10 bars (t 3.65). With cases at least 20 bars apart, 373 cases rise +3.31% over 20 bars (t 2.34). Yet the median trade lasts 1 day, and the book is invested on only 27% of days.
