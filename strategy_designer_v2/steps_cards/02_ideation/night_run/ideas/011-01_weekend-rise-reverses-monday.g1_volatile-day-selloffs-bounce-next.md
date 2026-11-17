---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's day-long fall is large compared with its usual daily move over the past 60 days, it rises over the next 1 day, and the larger the fall in units of its usual move, the larger the rise; the effect is stronger the higher the coin's recent 60-day volatility.
Consequence: A trader can lean long the day after a sharp fall in a volatile spell and refuse to sell into it, while expecting nothing similar after sharp rises.
Why:
- F1: Across all days and coins, the slope of the next day's excess return on the day's standardised return (its return over the mean absolute daily return of the past 60 days) steepens with the coin's volatility level: by volatility quartile it is +0.27e-3 (t 0.63), -1.32e-3 (t -2.80), -1.97e-3 (t -3.18) and -4.18e-3 (t -5.02), with about 3,600 days in each quartile.
- F2: In the top volatility quartile this reversal comes from down days only: the slope is -10.95e-3 (t -5.37, n 1,760) on days that fell and +1.07e-3 (t 0.71, n 1,866) on days that rose.
- F3: Graded by size over all days, the next day's excess return is +7.30e-3 after days at or below -2 usual moves (n 834) and +4.41e-3 after days between -2 and -1 (n 1,730), against only -0.5e-3 to -1.7e-3 after rises of any size.
- F5: The high-volatility reversal is negative in all 6 coins (t from -0.79 for XRP to -4.64 for XMR), but it is concentrated in early years (2018 t -4.50, 2020 t -4.86) and absent in 2023–2025 (t 0.56, -0.11, 0.14).
- F6: The weekend is not special: the next-day reversal slope after Sunday's return (-4.05e-3, t -4.00) is matched after Saturday's (-3.37e-3, t -4.13), Tuesday's (-2.79e-3, t -3.47) and Thursday's (-2.33e-3, t -3.29); and across Sunday sextiles the 2-day excess is not graded (-15.9e-3 in the mildest-rise sextile against -5.9e-3 in the largest), which is why the supporting check failed.
