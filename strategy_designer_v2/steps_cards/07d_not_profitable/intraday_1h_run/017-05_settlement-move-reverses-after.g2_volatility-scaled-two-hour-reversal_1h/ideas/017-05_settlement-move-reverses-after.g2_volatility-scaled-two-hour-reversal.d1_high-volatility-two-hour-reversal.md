---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 2-hour move is reversed over the next 2 hours by an amount that grows with the size of the move relative to its usual 2-hour move, and grows with the coin's 7-day hourly volatility, only while the coin's 7-day hourly volatility is high against its past month's level, where the reversal of the largest moves is several times its size in calmer weeks.
Consequence: A trader should fade 2-hour moves only in high-volatility weeks and stand aside in calm ones, where the reversal is smaller than the cost of trading it.
Why:
- F1: The book loses because of fees, not because the forecast fails. Its gain before fees averages 0.00234 a day (per-bar t 11.0), while fees average 0.0104 a day. That leaves a mean daily book return of -0.00803 and a Sharpe of -8.68 over 2,898 days.
- F2: The book trades far more than its edge can pay for. It turns over 0.40 of the book every hour, at about 10.7 bps of fee per unit of turnover. The 2-hour fade it trades earns only 3.36 bps per 2 hours across all bars (t 10.06, n 196,182), less than the cost of one round trip.
- F3: The gain sits in the large moves, but the book trades the small ones nearly as heavily. Gain before fees per bar rises from 0.0000005 in the lowest |forecast| quintile to 0.000302 in the highest, while turnover only rises from 0.31 to 0.52. The 2-hour fade on the top |move| decile earns 11.75 bps (t 7.44, n 19,620).
- F4: Volatility decides whether there is any reversal at all. For top-decile 2-hour moves, the next-2-hour fade earns 29.70 bps (t 7.68, n 6,542) in the highest 7-day-volatility tercile, against only 3.16 and 2.36 bps in the lower two. Yet the book turns over most in the calmest quintile (0.52 per bar, against 0.30 in the most volatile).
