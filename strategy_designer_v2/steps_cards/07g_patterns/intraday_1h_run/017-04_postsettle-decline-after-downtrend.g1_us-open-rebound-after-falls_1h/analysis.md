---
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
idea tested: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3559 USD
---
## Findings
- **F1:** The tested rebound is real but the fees eat it. Gross position gain is 0.000227 a day and fees are 0.000527 a day, so the book loses 0.00030 a day. Almost all fees are paid on the 11:00 and 13:00 bars, about 2.4 bp each, which is one full round trip every day.
- **F2:** From 16:00 UTC the coin continues its 3-day move rather than reversing it. The 2-hour return from the close of the 15:00 bar rises with the signed 72-hour return (pooled slope 0.0105, t = 7.3, n = 17018). It goes from −13.0 bp (t = −3.5) in the lowest quintile of 72-hour return to +20.3 bp (t = 6.4) in the highest. The slope is positive in 5 of 6 coins (t from 2.1 to 6.4; XRP −0.6) and holds from the 16:00 decision too (t = 4.5). It is weak from 2021 to 2024 (t between −0.1 and 1.8).
- **F3:** There is an unconditional rise from 20:00 to 22:00 UTC: the 20:00 bar averages +5.5 bp (t = 6.7) and the 21:00 bar +4.4 bp (t = 5.7). Every coin is positive (+2.7 to +8.8 bp; t = 2.4 to 2.6 for BTC, ETH, XRP and ZEC). The rise grows with the 3-day hourly volatility: +1.0 bp (t = 0.9) in the calmest quartile and +12.3 bp (t = 3.4) in the most volatile.
- **F4:** Outside the tested 11:00–13:00 hours, there is a second window where the coin runs against its 3-day move. The 2-hour return from the close of the 18:00 bar has slope −0.0094 on the signed 72-hour return (t = −6.9, n ≈ 17000), and from the 19:00 bar the slope is −0.0072 (t = −5.2). This is as strong as the tested hours (t of −7.8 and −9.0 at the 11:00 and 12:00 decisions).
- **F5:** I looked at about 24 hours across several tests, so I treat |t| below about 4 as possible chance. The hourly means near 13:00 (−3.6 bp, t = −3.8) and 02:00 (−2.8 bp, t = −3.8), the weekday split of the evening rise, and the year splits do not stand out enough to count.

## Ideas
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.g1_us-afternoon-trend-continuation` (from F2): For a coin, the return over the 2 hours from 16:00 UTC follows the direction of its 3-day return, and the larger its 3-day move, the larger that 2-hour move in the same direction.
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.g2_evening-drift-in-volatile-coins` (from F3): For a coin, the return over the 2 hours from 20:00 UTC is positive, and the higher the coin's hourly volatility over the past 3 days, the larger that rise.
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.g3_evening-fade-of-3-day-moves` (from F4, F1): For a coin, the return over the 2 hours from 19:00 UTC runs against its 3-day return: the larger its 3-day rise, the lower that return, and the larger its 3-day fall, the higher it is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
