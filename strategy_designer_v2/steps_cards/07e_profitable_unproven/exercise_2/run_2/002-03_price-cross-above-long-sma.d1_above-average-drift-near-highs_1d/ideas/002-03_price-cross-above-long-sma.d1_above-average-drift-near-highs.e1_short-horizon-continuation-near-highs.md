---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin closes above its long moving average, its next-day return is larger the closer the close sits to its recent closing high and the stronger its recent rise. The continuation is short-lived, carried in the days right after the close.
Consequence: Size longs up as the close presses its recent high in an uptrend, but expect the payoff over days rather than weeks and refresh the position often.
Why:
- F3: The edge sits at the one-bar horizon and grows with the forecast. The next-bar coin return is 4.6 and 4.4 bps in the two lowest in-market forecast quintiles, 22.2 and 22.7 bps in the middle two, and 44.8 bps in the top quintile. There the position's gain is 49.3 bps per bar against 0.2 bps in the lowest (n ≈ 1,539 each).
- F2: The idea's own 20-bar horizon shows nothing. On the non-overlapping 20-bar grid, the excess return in the trending regime is +0.0023 (t 0.14, n 408) against −0.0022 (t −0.21, n 419) outside it. Forecast buckets are not monotone: +0.023, −0.052, −0.026 and +0.072 from low to high, with no |t| above 1.6.
- F4: Nearly all the gain came in moderate uptrends. Bars whose past 60-day rise lies in (0, 0.2] carry 49% of the summed gain and those in (0.2, 0.5] carry 48%. In the (0, 0.2] state, the next-bar return while in the market is 49.6 bps against 14.7 bps on all bars of that state. Bars after 60-day falls contribute −1.3% of the gain.
