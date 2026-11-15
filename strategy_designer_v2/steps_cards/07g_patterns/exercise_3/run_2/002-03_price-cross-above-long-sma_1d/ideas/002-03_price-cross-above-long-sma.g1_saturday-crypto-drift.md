---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, the close-to-close return over the UTC Saturday is higher than its return over the other days of the week, so the coin's next 1-day return is larger when the coming day is a Saturday.
Consequence: A trader long a coin should hold or add exposure into the Saturday session and refuse to cut longs on Friday's close, if Saturday's mean return is confirmed above the other days'.
Why:
- F1: Saturday (UTC) is the one weekday whose coin return stands out: averaged across the six coins it is +0.46% on 414 days (t 3.07), against between −0.17% and +0.32% on the other six weekdays, and it holds after the top 1% of days are removed (+0.23%, t 3.48, while Monday, Tuesday and Thursday turn negative).
- F2: The Saturday excess is broad rather than a few outliers: Saturday minus other days is positive in all six coins (LTC t 2.67, XMR 1.82, ZEC 1.77, ETH 1.59, XRP 1.42, BTC 0.34), in 7 of 8 years (only 2023 negative, t −0.67) and in all four window groups (w7–12 t 2.66, w19–24 t 1.78); Saturday's median return is +0.19% against 0.00% on other days, and its hit rate is 55.0% against 50.0%.
- F3: The book's own daily return peaks on Saturday (+0.20%, t 2.78 over 414 days), the largest of any weekday. The strategy has no calendar input, so this gain comes from being long on the day the coins rise most.
