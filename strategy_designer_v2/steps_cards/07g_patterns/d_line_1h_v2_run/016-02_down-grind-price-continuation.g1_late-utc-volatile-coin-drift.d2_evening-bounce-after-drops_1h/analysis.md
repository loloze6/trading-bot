---
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
idea tested: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3860 USD
---
## Findings
- **F1:** The two hours after the 21:00 UTC close rise whether or not the coin fell. The hour-20 and hour-21 bars are the two strongest hours of the day (mean 0.000545, t 6.75, n 17403; and 0.000436, t 5.66, n 17417). The 2-hour return is positive in every coin (0.00082 to 0.00114, t 3.1 to 4.7, about 2750 cases each) and in 79 % of windows. It also holds after rises: the top vol-scaled-return decile gives 0.0017 (t 4.1, n 1641), and the Spearman correlation between the size of a rise and the return is -0.004.
- **F2:** That 2-hour rise after 21:00 grows with the coin's 7-day hourly volatility. By per-coin volatility quartile it is 0.00030 (t 2.35), 0.00079 (t 4.87), 0.00079 (t 3.64) and 0.00211 (t 6.49), about 4100 cases each.
- **F3:** The rise after 21:00 follows the size of the past 24-hour move, not its sign. By quintile of the absolute vol-scaled 24-hour return it is 0.00109, 0.00044, 0.00034, 0.00142 and 0.00169 (top quintile t 5.47, n 3281). After falls, the fall's depth correlates only weakly with the return (Spearman 0.061).
- **F4:** The book loses although the timing is real. Summed gross position gains of 5.34 are outweighed by summed fees of -7.81, and per-trade gross P/L runs from +0.09 % (BTC) to -0.07 % (XRP) against about 0.1 % of commission per trade. The book's daily Sharpe is -0.67 and its mean daily return is -0.00014.
- **F5:** Over the next 24 hours, the coin's past 24-hour vol-scaled return predicts a reversal. The OLS slope is -0.0019 (t -4.72, n 15950, non-overlapping daily cases). The lowest vol-scaled-return quintile is followed by roughly +0.004 to +0.007 over 24 hours, the highest by -0.0017 to +0.0002.
- **F6:** Days whose 24-hour move was spread evenly across hours are followed by larger 3-day returns than days dominated by one hour, whatever the move's direction. Grouped by the share of the day's absolute hourly moves taken by the largest hour, the next 72-hour return is 0.0061 (t 5.13), 0.0040 (t 3.42) and 0.0001 (t 0.11), n about 5317 each. High minus low is -0.0060, Welch t -3.72. Over 24 hours the same gap is weaker (t -1.39).
- **F7:** Two other hours fall consistently across the pooled coins: the hour-13 bar (-0.000356, t -3.80) and the hour-2 bar (-0.000277, t -3.80), each with about 17400 cases.

## Ideas
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g1_volatility-scaled-evening-utc-rise` (from F1, F2, F3, F4): Each coin rises over the two hours after 21:00 UTC, and the higher its 7-day hourly volatility at that close, the larger the rise.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g2_daily-vol-scaled-drop-reversal` (from F5, F4): The deeper a coin's 24-hour return falls in units of its 7-day hourly volatility, the larger its rise over the next 24 hours.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g3_even-step-days-precede-gains` (from F6): The more evenly a coin's absolute hourly moves over the past 24 hours are spread across the hours, the larger its rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
