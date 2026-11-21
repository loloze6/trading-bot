---
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
idea tested: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4075 USD
---
## Findings
- **F1:** Closes nearest the top of their 30-day range are followed by a 5-day rise beyond the coin's normal drift. In the top quintile of the position in the 30-day range, the mean unusual 120-hour move is +1.47 % (t 2.81, 624 non-overlapping cases), and over 240 hours it is still positive on 5 of 6 coins (XRP +8.2 % t 2.57, BTC +1.9 % t 1.81). The four lower quintiles run from −0.97 % to −0.19 %, and the cost of a trade is 0.19 %.
- **F2:** F1's edge is uneven across time and coins. It is +2.83 % (t 3.25, 297 cases) in windows w13–w24 against +0.23 % (t 0.38, 327 cases) in w1–w12. It is positive on 5 of 6 coins over 120 hours, with LTC the exception at −0.51 %.
- **F3:** Large 1-hour falls are followed by a rebound. After a 1-hour fall of 1.5 to 3 times the coin's 30-day hourly standard deviation, the next 24 hours rise +0.65 % beyond drift (t 2.86, 789 cases), and after falls beyond 3 times they rise +0.62 % (t 1.14, 160). Small rises (0 to 1.5) are followed by −0.17 % (t −2.90, 7112). That is a reversal graded on the falling side, with the rebound about 3.4 times the cost of a trade.
- **F4:** The tested surge carries little. The top quintile of the 24-hour surge, divided by its 30-day mean absolute value, gives +0.94 % over 120 hours (t 1.77, 624 cases). It is positive on all 6 coins but has t at or below 1.41 on each, is similar in both halves (+0.91 % and +0.97 %), and the lower quintiles are not ordered (−0.90 % to +0.14 %).
- **F5:** The book's gain does not grow with the size of its signal. The net profit per trade by entry-forecast quartile is U-shaped: 4.60 %, 2.05 %, 2.95 % and 5.00 % (1304 trades each).
- **F6:** The hours 21 and 22 UTC rise on every coin. They gain +3.8 to +4.9 bps per hour beyond drift on all 6 coins (t 2.6 to 4.0, about 5800 hours each), and +7.06 bps (t 8.09) in w13–w24 against +1.64 bps (t 2.38) in w1–w12. That is about 8 to 10 bps for the two hours, at or below a round trip, so this is no idea of its own (as with findings F2 and F10).
- **F7:** High relative volatility goes with a rise only in the later windows. In the top quintile of 30-day hourly volatility over its 90-day mean, the unusual 120-hour move is +1.23 % (t 2.39, 506 cases). It is +2.01 % (t 2.68) in w13–w24 and −0.18 % (t −0.36) in w1–w12, and with about forty tables examined this does not stand apart from chance well enough to carry an idea.

## Ideas
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.g1_near-month-high-five-day-continuation` (from F1, F2): The nearer a coin's hourly close is to the top of its 30-day high-low range, the more the coin rises over the next 5 days beyond its usual 5-day return.
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.g2_sharp-hourly-drop-rebound` (from F3): The larger a coin's fall over the last hour, measured against its usual hourly move over the past 30 days, the more the coin rises over the next 24 hours beyond its usual 24-hour return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
