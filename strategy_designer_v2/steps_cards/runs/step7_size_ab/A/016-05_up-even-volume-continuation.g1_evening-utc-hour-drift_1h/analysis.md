---
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3364 USD
---
## Findings
- **F1:** The book loses to its fees, not to its forecast. Before costs the positions earn +2.18 bp per coin-day (every coin positive, from +0.25 bp on LTC to +2.90 bp on ETH), while fees take 10.49 bp per coin-day. The book's mean daily return is therefore -8.4 bp, against +11.9 bp a day for holding the coins.
- **F2:** The edge per trade is far smaller than its cost. The case from the 19:00 bar's close over 2 hours gains 2.7–8.8 bp by coin, with strength 0.014–0.050 (about 0.035 on average). Each trade is a full round trip held about 120.6 minutes, and fees average 0.100 % of the trade (≈10 bp each side), so the gross move is roughly a third of the round-trip cost.
- **F3:** The book trades almost every day. There are 17,075 trades, all long, at 0.97 per coin-day. They pay fee bars of about 5.3 bp of book at both the 19:00 open (16,957 bars) and the 21:00 close (16,956 bars), with the position sized at a mean of 0.50 of the book.
- **F4:** The effect sits almost entirely in the coin's most volatile weeks. By quintile of 7-day hourly volatility, the 2-hour case returns 1.5, 3.2, -0.8, 1.7 and 18.5 bp, with strength 0.008, 0.018, -0.013, 0.005 and 0.120. The book's gross gain per active bar is about 0.0–0.4 bp in quintiles 0–3 and 4.38 bp in quintile 4, where its fee per bar is 2.02 bp.
- **F5:** The evening rise is uneven across years. Strength is -0.054 in 2018, 0.089 in 2020, 0.106 in 2021, -0.027 in 2023 and between 0.017 and 0.045 in the others. The cause holds in every period, which is why every leave-one-out Sharpe stays negative (-3.0 at best).
- **F6:** The recorded trades read worse than the bars. Their gross mean is -0.064 % (median -0.054 %, t -5.9 over 17,075 trades), against +5–6 bp at the bar closes, so fills may be worse than the decision close, which deepens the cost gap.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_evening-drift-in-volatile-weeks` (from F1, F2, F3, F4): Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours. The rise is larger the higher its realised hourly volatility over the past 7 days, only while that volatility stands well above the coin's own usual level of the past several months, and there it grows steeply with volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
