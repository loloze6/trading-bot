---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 5-day average volume against its 30-day average, the higher its return over the next 3 days, whatever the direction of its last 5 days.
Consequence: A trader would lean long a coin whose recent volume is heavy against its month and away from a coin trading on thin volume, instead of reading thin volume only as a warning on dips.
Why:
- F1: Over all bars, not only after 5-day falls, the 5-day/30-day log volume ratio predicts the coin's excess 3-day return upward: the pooled slope is 0.0124 (t 4.32, n 4283 non-overlapping cases); it is 0.0170 after falls (t 4.07, n 2071) and 0.0072 after rises (t 1.80, n 2212), while the ratio multiplied by the sign of the 5-day return gives t -1.99, so the effect follows volume, not the fall the idea names.
- F2: The volume-ratio effect holds at 7 days too (slope 0.0233, t 3.22, n 1723), but it is concentrated in a few places: XRP (t 3.75) and ZEC (t 2.36), against t 0.36 to 1.32 for BTC, ETH, LTC and XMR, and windows w19-24 (t 4.39) against t 1.00 to 1.92 in the other three window groups.
- F5: The book's mean daily return of 0.00017 sits far below the coins' own mean daily returns of 0.00067 to 0.00155, because it is short on 28-36 % of bars against long on 18-21 % (mean position -0.035 to -0.086); its gain from the market's own rise is -0.000076 a day.
