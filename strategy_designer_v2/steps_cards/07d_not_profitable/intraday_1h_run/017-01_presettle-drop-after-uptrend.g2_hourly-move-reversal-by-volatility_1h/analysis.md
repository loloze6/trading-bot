---
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2784 USD
---
## Findings
- **F1:** The book loses because fees swamp a real but tiny edge: per bar the position earns 0.79 bps before costs but pays 6.54 bps in fees, because it turns over 0.61 of the book every hour at 10.7 bps per unit of turnover (20.77 trades per day). That gives a mean daily return of -0.0136 and a Sharpe of -16.35, against holding's 0.55 over 2,898 days.
- **F2:** The one-hour reversal is real but far too small to trade hourly: the sign-adjusted next-hour return is 1.79 bps on average and 3.12 bps in the top quintile of |vol-scaled move| (slope t 11.48, 413,189 cases). Even the strongest hours earn under a third of the 10.7 bps it costs to turn the position over fully.
- **F3:** Every coin loses in the same way: the gain before costs is 0.12 to 1.34 bps per bar (ETH lowest, ZEC highest), while fees are 5.6 to 7.6 bps per bar. The failure is the trading speed, not one coin or one window; the lowest Sharpe with one window left out is still -16.86.
- **F4:** The forecast's information outlasts the hour it is traded on. For the top quintile of |forecast|, the sign-adjusted return is 5.78 bps over the next 4 hours (t 3.95, 21,204 non-overlapping cases) and 28.3 bps over the next 24 hours (t 3.62, 4,015 cases), against 2.63 bps over the next 1 hour.
- **F5:** A slower form of the same reversal also shows up. The coin's 24-hour return scaled by its volatility reverses over the next 24 hours with a slope of 17.9 bps per unit (t 4.36, 17,102 cases), and its top quintile reverses by 22.8 bps. The sign is not stable across horizons, though: at 12 hours the slope is -6.6 bps per unit (t -3.28), and at 48 hours it is -12.2 bps per unit (t -1.49).

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-fades-over-day` (from F1, F2, F4): The larger a coin's last 1-hour return relative to its 24-hour volatility, the more its return runs the opposite way, with the reversal building beyond the next 1 hour to its largest size over the next 24 hours.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_daily-vol-scaled-move-reversal` (from F1, F3, F5): The larger a coin's 24-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
