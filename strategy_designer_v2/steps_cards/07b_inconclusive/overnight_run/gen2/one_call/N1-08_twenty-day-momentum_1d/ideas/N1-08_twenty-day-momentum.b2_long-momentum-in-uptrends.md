---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.b inconclusive
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its 50-day average and its 20-day return is positive, its price rises over the next 20 daily bars.
Consequence: A trader should take momentum only on the long side, and only while price holds above the 50-day average, keeping in mind that this mostly harvests trend drift and can fail in a falling year.
Why:
- F2: The two sides pull in opposite directions. Long bars have a mean signed forward return of +0.027 (t = 1.67, n = 400). Short bars have -0.023 (t = -2.20, n = 427), so shorting after 20-day falls loses money, and the slope inside the short side is t = -2.65.
- F5: Long forecasts when the close is above its 50-day average have a mean forward 20-bar return of +0.037 (t = 2.40, n = 221). Their excess over each coin's own mean is only +0.012 (t = 0.78), so most of the gain is the coins' upward drift and not added persistence. The same group lost in 2022 (-0.061, t = -2.34, n = 31).
- F6: The effect is unstable over time and noisy. The yearly slope t runs from -2.90 (2023) to +1.48 (2025), with 6 of 8 years negative. The top forecast fifth has nearly twice the dispersion of the others (forward sd 0.41 vs 0.21 to 0.25).
