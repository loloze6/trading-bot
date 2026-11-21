---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 1-day return is reversed over the next 1 day by an amount that grows with the size of that return relative to its usual 1-day move, while the coin's 7-day hourly volatility is high against its past month's level.
Consequence: In volatile weeks, fading the day's large move and holding it for a day captures a reversal of the order of a percent, with far fewer trades than an hourly fade.
Why:
- F1: The book loses because of fees, not because the forecast fails. Its gain before fees averages 0.00234 a day (per-bar t 11.0), while fees average 0.0104 a day. That leaves a mean daily book return of -0.00803 and a Sharpe of -8.68 over 2,898 days.
- F2: The book trades far more than its edge can pay for. It turns over 0.40 of the book every hour, at about 10.7 bps of fee per unit of turnover. The 2-hour fade it trades earns only 3.36 bps per 2 hours across all bars (t 10.06, n 196,182), less than the cost of one round trip.
- F5: The reversal is much larger and slower at the 1-day scale. Fading the top-decile 24-hour move over the next 24 hours earns 51.68 bps (t 3.20, n 1,626). In the highest volatility tercile it earns 198.95 bps (t 5.14, n 543), while in the low and middle terciles it loses 28.41 and 15.89 bps.
