---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After the short moving average crosses below the long one, the coin drifts down mainly in the first two weeks after the cross. The drift is absent at later bars of the same spell.
Consequence: A trader should take the short only right after a real downward cross and close it within about two weeks, not hold it for the life of the death-cross state.
Why:
- F8: Only the youngest part of a short spell pays. The first 10 bars earn +0.000517 a bar (t 0.55). Bars 10–30 of a spell lose -0.001893 (t -2.48), bars 30–60 lose -0.000943, and bars 60–120 lose -0.000481, so the cross's information, if any, fades within about two weeks while the position is kept for months.
- F4: The trades are few and long, and their losses dwarf their fees: 1273 trades, all short, held a median of 23 days (mean 36), with a mean gross P/L of -11.2% against a mean commission of 0.20%, a gross win rate of 23.9%, and a median trade of -8.1%. The 10–30 day trades are the worst at -16.1% on average.
- F3: A larger forecast loses more in the book: the bottom |forecast| quartile (mean forecast -0.38) earns +0.000074 gross a bar, while the top quartile (mean -15.9) earns -0.002029. At the trade level, small-entry trades average -12.8%, mid-entry trades -13.4% and large-entry trades -7.4%. This is the reverse of the plan's supporting tercile check, which passed at +0.0071.
- F10: The standardised forecast is not tied to an actual death cross: the shallowest quartile of short bars has a mean raw spread of +36.7 (short average above the long one) with a forecast of -0.63, so some shorts fire merely because the spread is below its own 200-bar mean. That quartile earns about zero gross (-0.000026).
