---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3485 USD
---
## Findings
- **F1:** The book fails only on Calmar: 0.698 against the 0.75 bar. Its daily chain returns 18.5 % a year with a deepest fall of -26.6 % (w8 into w9, 119 days to the trough). The other deep falls are mostly in falling markets: in w16 the book lost a summed -0.26 while the coins summed -0.82, and from w12 to w14 it lost -0.21 while the coins summed -0.78.
- **F2:** The rebound after a one-day drop is absent when recent volatility is compressed. In the lowest quintile of 20-day over 60-day realised volatility, active bars have a next-day excess return of -0.0033 (t -2.60, n 1431), a mean position gain of -0.0010 and a slope on the forecast of -0.00016 (t -0.68). In the highest quintile the excess return is +0.0063 (t 4.61) and the slope is +0.00059 (t 2.96). The gain rises steadily across the quintiles (-0.0010, 0.0012, 0.0021, 0.0024, 0.0046).
- **F3:** The interaction regression of next-day excess return on forecast, volatility ratio and their product gives the product a t of 3.45. The forecast alone gets a t of -2.37. So the drop's size predicts a rebound only in proportion to how expanded recent volatility is.
- **F4:** Recent high-low ranges grade the outcome the same way. Over the quintiles of the 10-day over 60-day mean range, the active bars' excess return runs from -0.0036 (most compressed) to +0.0079 (most expanded), and the mean gain from -0.0014 to +0.0062.
- **F5:** Scaling each position by the volatility ratio (clipped 0 to 2) lifts the pre-fee book from a mean of 0.00092 to 0.00112 and a yearly return from 34.4 % to 44.0 %. Calmar rises from 1.45 to 1.90, but the deepest fall barely moves (-23.8 % to -23.2 %). The Calmar gain comes through the yearly return, not through shallower falls.
- **F6:** The book's worst 5 % of days lose about evenly across the volatility-ratio quintiles (summed losses of -4.5, -4.0, -5.5, -5.4 and -6.0). The deep falls are therefore not confined to compressed markets.
- **F7:** Fees and turnover take a large share of the gain. The book earns 0.00058 a day after costs against 0.00092 before, and it trades on 0.39 of the bars.
- **F8:** The rebound is concentrated in the extremes of the 20-day trend. Excess return is +0.0043 (t 2.51) in the most fallen quintile and +0.0047 (t 3.43) in the most risen, while the middle three quintiles sit near zero (-0.0006 to +0.0004).

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.d1_drop-rebound-in-expanded-volatility` (from F1, F2, F3, F5, F6): The larger a coin's fall over the last 1 day, the higher its return over the next 1 day, only while the coin's realised volatility over the last 20 days is high against its last 60 days, the rebound growing with that ratio.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.d2_drop-rebound-in-wide-ranges` (from F1, F4, F7): The larger a coin's fall over the last 1 day, the higher its return over the next 1 day, only while the coin's mean daily high-low range over the last 10 days is wide against its last 60 days, the rebound growing with that range ratio.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.d3_drop-rebound-after-strong-trends` (from F1, F7, F8): The larger a coin's fall over the last 1 day, the higher its return over the next 1 day, only while the size of its 20-day return, up or down, is large, the rebound growing with that size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
