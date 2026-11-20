---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours after 21:00 UTC, and the higher its 7-day hourly volatility at that close, the larger the rise.
Consequence: A trader would lean long into the 21:00 UTC close with size scaled up by the coin's recent volatility, whatever its 24-hour direction, because the move is too small to pay costs in calm coins.
Why:
- F1: The two hours after the 21:00 UTC close rise whether or not the coin fell. The hour-20 and hour-21 bars are the two strongest hours of the day (mean 0.000545, t 6.75, n 17403; and 0.000436, t 5.66, n 17417). The 2-hour return is positive in every coin (0.00082 to 0.00114, t 3.1 to 4.7, about 2750 cases each) and in 79 % of windows. It also holds after rises: the top vol-scaled-return decile gives 0.0017 (t 4.1, n 1641), and the Spearman correlation between the size of a rise and the return is -0.004.
- F2: That 2-hour rise after 21:00 grows with the coin's 7-day hourly volatility. By per-coin volatility quartile it is 0.00030 (t 2.35), 0.00079 (t 4.87), 0.00079 (t 3.64) and 0.00211 (t 6.49), about 4100 cases each.
- F3: The rise after 21:00 follows the size of the past 24-hour move, not its sign. By quintile of the absolute vol-scaled 24-hour return it is 0.00109, 0.00044, 0.00034, 0.00142 and 0.00169 (top quintile t 5.47, n 3281). After falls, the fall's depth correlates only weakly with the return (Spearman 0.061).
- F4: The book loses although the timing is real. Summed gross position gains of 5.34 are outweighed by summed fees of -7.81, and per-trade gross P/L runs from +0.09 % (BTC) to -0.07 % (XRP) against about 0.1 % of commission per trade. The book's daily Sharpe is -0.67 and its mean daily return is -0.00014.
