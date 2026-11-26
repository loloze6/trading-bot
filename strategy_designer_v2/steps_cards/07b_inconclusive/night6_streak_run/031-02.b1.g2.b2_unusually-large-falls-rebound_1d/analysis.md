---
line: 7.b inconclusive
backtest: 031-02.b1.g2.b2_unusually-large-falls-rebound_1d
idea tested: 031-02.b1.g2.b2_unusually-large-falls-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3204 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: the slope of the 2-day return minus drift on the forecast is +0.00039 with a day-clustered t of 1.81 (8,650 grid bars, 4,217 with a positive forecast over 1,125 days), and the top fifth of positive forecasts beats the drift by +0.73 % (t 1.69, 844 cases on 297 days), so the effect points the predicted way but is too small for six coins to show clearly.
- **F2:** The effect is spread across most coins, not confined to one. At 2 days the slope is positive on 4 of 6 coins: XRP t 2.43, LTC 1.86, ZEC 1.59 and XMR 1.57, while BTC (t -0.32) and ETH (t -0.02) are flat. It is also positive in 7 of 8 years, each year's t below 1.2, with 2022 the one negative year (t -0.72). This is a small, broad effect that more coins and days would sharpen, not one living in a single part of the data.
- **F3:** The effect is clearest at the 1-day horizon and fades as the horizon lengthens: the slope's t is 3.57 at 1 day (17,380 cases), 1.81 at 2 days, 1.04 at 3, -0.11 at 5 and 1.05 at 10.
- **F4:** At 1 day, all 6 coins have a positive slope (XMR t 5.04, XRP 3.27, LTC 2.32, ZEC 2.30, ETH 1.85, BTC 1.49), and 7 of 8 years are positive (2025 is -0.32).
- **F5:** The rebound is graded with the size of the fall measured in the coin's own 60-day standard deviations. At 1 day the move beyond drift rises from -0.04 % after falls of 0 to 0.5 sd, to +0.26 % after 0.5 to 1 sd, +0.65 % after 1.5 to 2 sd, +0.85 % after 2 to 3 sd (t 2.03, 259 cases), and +2.35 % after falls above 3 sd (75 cases).
- **F6:** The plan's forecast standardises the scaled fall against its own past 61 values, which blurs the grading: its lower three positive quintiles at 2 days sit below drift (-0.13 %, -0.37 %, -0.29 %). The raw scaled fall that the idea names gives a slope t of 2.23 at 2 days and 2.61 at 1 day.
- **F7:** The pooled unusual move per case (+0.15 %, t 0.86) is 0.8 times the 0.19 % cost of a trade. The top-fifth forecasts carry +0.69 % at 1 day and +0.73 % at 2 days beyond drift, several times the cost. So the trade is worth taking only on the most unusual falls, and only if the effect holds on more data.

## Ideas
- `031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins` (from F1, F2, F7): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 2 days.
- `031-02.b1.g2.b2.b2_unusual-falls-rebound-next-day` (from F3, F4, F5, F6, F7): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
