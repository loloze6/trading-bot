---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
idea tested: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3879 USD
---
## Findings
- **F1:** The idea's move per case is smaller than one trade's cost. Over 24 hours the move is +0.13 % in total (+0.14 % unusual) against a cost of 0.19 %. The book pays fees of 3.6 to 9.6 bps a day per coin but earns only 1.8 bps a day on average, -2.4 to +6.7 bps by coin. Every coin underperforms holding, which earns 6.7 to 15.5 bps a day. That is why the book's gain against holding and its mean daily return fail.
- **F2:** The reversal sits almost entirely in volatile conditions. Settlement cases in each coin's top third by 20-hour volatility gain 34 bps of excess over 24 hours (t 4.1, 5755 cases). The bottom and middle thirds gain 2.1 and 2.2 bps (t 0.4). Inside the volatile third, the largest third of pre-settlement moves gains 61 bps (t 4.0, 1955 cases), about 3 times a trade's cost, while the quiet, smallest-move cell loses 21 bps (t -2.6).
- **F3:** The size of the pre-settlement move grades the reversal. By quintile of |move| in usual 2-hour moves, the 24-hour excess is 1, 3, 4, 30 and 26 bps (t 3.6 and 2.9 in the top two quintiles), so the lower 60 % of cases carry under a quarter of the cost each.
- **F4:** Volatility measured against the coin's own past also sorts the cases. With the 30-day hourly volatility over its 6-month median split in thirds, the 24-hour excess is -11 bps (t -1.4), +16 bps (t 1.9) and +23 bps (t 2.5).
- **F5:** The effect is not specific to the funding clock. The 17 UTC placebo hour reverses as much as 00 UTC over 24 hours (12.0 vs 12.9 bps, t 3.3 vs 3.4). Among high-volatility, large-move cases, 05 UTC gives 51 bps (t 2.7) and 11 UTC 36 bps (t 2.1), against 61 bps at 00 UTC.
- **F6:** The reversal is larger when the bet points with the coin's 7-day trend, that is, when the move into settlement ran against the week's direction. Those cases gain 24 bps (t 4.2, 7571 cases), against 3 bps (t 0.6, 8531 cases) when the bet goes against the 7-day trend.
- **F7:** The effect rests on 2018 to 2020 and on volatile coins.

## Ideas
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal.d1_volatile-day-settlement-reversal` (from F1, F2, F3, F4): The 2-hour return into the 00 UTC funding settlement runs opposite to the return over the 24 hours after it, and the larger the pre-settlement move relative to the coin's usual 2-hour move, the larger the move back. This holds only while the coin's hourly moves over the past 20 hours are large against its own usual level, and the move back grows with that volatility.
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal.d2_counter-trend-settlement-move-reverses` (from F1, F3, F6): The 2-hour return into the 00 UTC funding settlement runs opposite to the return over the 24 hours after it, and the larger the pre-settlement move relative to the coin's usual 2-hour move, the larger the move back. This holds only while that 2-hour move runs against the coin's 7-day return.
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal.d3_volatile-two-hour-move-reversal` (from F2, F3, F5): At any hour of the day, a coin's 2-hour return runs opposite to its return over the next 24 hours. The larger that 2-hour move relative to the coin's usual 2-hour move, and the higher the coin's hourly volatility over the past 20 hours against its usual level, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
