---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would take a daily position against unusually large one-day moves, sized to the move's size in volatility units, trading about once a day instead of every hour.
Why:
- F1: The book loses because fees swamp a real but tiny edge: per bar the position earns 0.79 bps before costs but pays 6.54 bps in fees, because it turns over 0.61 of the book every hour at 10.7 bps per unit of turnover (20.77 trades per day). That gives a mean daily return of -0.0136 and a Sharpe of -16.35, against holding's 0.55 over 2,898 days.
- F3: Every coin loses in the same way: the gain before costs is 0.12 to 1.34 bps per bar (ETH lowest, ZEC highest), while fees are 5.6 to 7.6 bps per bar. The failure is the trading speed, not one coin or one window; the lowest Sharpe with one window left out is still -16.86.
- F5: A slower form of the same reversal also shows up. The coin's 24-hour return scaled by its volatility reverses over the next 24 hours with a slope of 17.9 bps per unit (t 4.36, 17,102 cases), and its top quintile reverses by 22.8 bps. The sign is not stable across horizons, though: at 12 hours the slope is -6.6 bps per unit (t -3.28), and at 48 hours it is -12.2 bps per unit (t -1.49).
