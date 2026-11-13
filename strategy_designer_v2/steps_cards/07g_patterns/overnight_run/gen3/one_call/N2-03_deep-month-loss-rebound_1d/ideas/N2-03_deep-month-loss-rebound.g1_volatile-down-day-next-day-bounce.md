---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.g patterns
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close falls by at least one of its own 20-day standard deviations while its 20-day volatility is in its upper range, the next day's return is higher than the coin's usual daily return. The bounce is larger after two such down days in a row.
Consequence: A trader can buy a high-volatility, unusually large down close for a one-day hold and skip the same signal in calm periods.
Why:
- F1: After a day whose return is at least one 20-day standard deviation below zero, the next day's return beats the coin's mean by 0.0050 when the 20-day change is negative (n=1200, t=3.05, hit 59%). It beats it by 0.0064 when the 20-day change is positive (n=635, t=3.25, hit 60%). On days that are not down by one standard deviation, the excess is -0.0008 (n=12665, t=-1.93). The one-day rebound is local and independent of the month's fall that the idea uses.
- F2: This one-day rebound after a down day of one standard deviation or more grows with the coin's 20-day volatility. The next-day excess is -0.0020 in the lowest volatility tercile (n=683, t=-1.33), 0.0043 in the middle (n=610, t=2.15) and 0.0164 in the highest (n=542, t=5.31). With events spaced at least 5 bars apart, the high-volatility next-day mean is 0.0087 (n=377, t=2.58).
- F4: When the down day follows another down day of one standard deviation or more, the next-day excess is 0.0144 (n=260, t=3.49, hit 64%). After a single down day it is 0.0039 (n=1534, t=2.92).
- F5: The rebound appears in all six coins (next-day excess 0.0021 to 0.0098; XMR t=3.54, n=314). It is strongest in 2020 and 2021 (0.0149 and 0.0144, t of about 3.4 each) and fades in 2024 and 2025 (-0.0014 and 0.0028, t below 1).
