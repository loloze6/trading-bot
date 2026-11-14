---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA of the close is above the 200-day SMA, the coin keeps drifting upward, and the more so the larger its recent-weeks rise, except that the drift per unit of risk shrinks as that recent rise becomes extreme.
Consequence: A trader would let exposure grow with the recent rise but less than in proportion at the top, which cuts the full-size single-day blows that follow the strongest runs.
Why:
- F3: When the forecast is positive, the next 10 bars' return above holding rises with the coin's prior 20-bar return: slope 0.103, t 3.74, 694 independent blocks. By quartile of that prior return it runs from -2.94% (t -2.73) in the falling quartile to +3.39% (t 1.83) in the strongest. In flat blocks the same slope is -0.018 (t -0.74).
- F6: The book's 100 worst single days come at full size after strong runs. Mean allocation was 0.99 and mean forecast 17.6, with 80% at forecast above 15 against 27% of all long days, and the mean prior 20-day return was +14.7% against +4.6% on all long days.
