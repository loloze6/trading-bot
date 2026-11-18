---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the last 1 day, the higher its return over the next 1 day, only while the coin's mean daily high-low range over the last 10 days is wide against its last 60 days, the rebound growing with that range ratio.
Consequence: A trader would lean long after a drop that lands inside widening daily ranges, sizing with the drop and the range expansion, and would stay out after drops from tight ranges.
Why:
- F1: The book fails only on Calmar: 0.698 against the 0.75 bar. Its daily chain returns 18.5 % a year with a deepest fall of -26.6 % (w8 into w9, 119 days to the trough). The other deep falls are mostly in falling markets: in w16 the book lost a summed -0.26 while the coins summed -0.82, and from w12 to w14 it lost -0.21 while the coins summed -0.78.
- F4: Recent high-low ranges grade the outcome the same way. Over the quintiles of the 10-day over 60-day mean range, the active bars' excess return runs from -0.0036 (most compressed) to +0.0079 (most expanded), and the mean gain from -0.0014 to +0.0062.
- F7: Fees and turnover take a large share of the gain. The book earns 0.00058 a day after costs against 0.00092 before, and it trades on 0.39 of the bars.
