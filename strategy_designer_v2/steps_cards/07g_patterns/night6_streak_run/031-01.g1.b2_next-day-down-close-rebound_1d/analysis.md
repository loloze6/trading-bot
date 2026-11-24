---
line: 7.g patterns
backtest: 031-01.g1.b2_next-day-down-close-rebound_1d
idea tested: 031-01.g1.b2_next-day-down-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4018 USD
---
## Findings
- **F1:** How low a coin closes within its day's range predicts the next day apart from the size of the day's fall. In a regression of the next day's excess return on the volatility-scaled return, the close location, the range and the volatility rank, the close location has a coefficient of -0.0083 with t -2.81, while the scaled return itself falls to t 0.47. Pooled over both sides, a score of (0.5 - close location) x 2 times the excess return averages +0.12 % with a day-summed t of 1.96 over 1002 days.
- **F2:** The close-location gradient holds on down days and on up days separately. On down days, the next-day excess return runs from +0.52 % (1137 bars, closes in the bottom fifth of the range) to -0.34 % (42 bars, top fifth). On up days it runs from +0.31 % (64 bars) to -0.04 % (1159 bars).
- **F3:** Among the biggest third of scaled falls, the next-day excess return depends on where the day closed. It is +0.77 % when the close is in the lower third of the day's range (531 bars) and -0.55 % when the close is in the upper third (114 bars). So the tested rebound is carried by falls that close near the low.
- **F4:** The close-location effect is not uniform. Bottom-fifth minus top-fifth next-day excess return is positive in 6 of 8 years (+2.0 %, +1.3 %, +2.4 %, +0.05 %, +1.2 %, +0.5 %) and negative in 2021 and 2024 (-0.4 %, -0.5 %). By coin it is positive for BTC, ETH, LTC and XMR (+0.4 % to +1.6 %) and negative for XRP and ZEC (-0.6 %, -0.2 %).
- **F5:** A day's range that is wide against the coin's usual daily move is followed by a rise. The widest fifth of range over 60-day volatility is followed by +0.40 % excess return the next day (t 3.62, 2900 bars), against -0.09 % to -0.16 % for the three narrowest fifths. In the joint regression the range keeps t 2.15. A long upper wick (top fifth of high-to-close in usual moves) is followed by +0.61 % (1201 bars).
- **F6:** The close-location effect lasts one day only. On non-overlapping 3-day stretches, the lowest-close fifth is followed by -0.23 % excess (1145 cases), against +0.26 % for the fourth fifth.
- **F7:** The book's best and worst held days both follow the deepest falls. The bottom gain decile followed an average z of -1.20 and a close location of 0.26; the top gain decile followed z -1.47 and close location 0.23. The bet's large swings sit on the same bars that carry its edge, consistent with its Calmar of 0.73 falling short of 0.75.
- **F8:** Two other patterns did not hold across years, so they are not findings to build on:

## Ideas
- `031-01.g1.b2.g1_close-near-low-rebounds` (from F1, F2, F3, F4, F6): The lower a coin closes within its day's high-to-low range, the more it rises above its normal drift over the next 1 day. This holds on down days and on up days alike, and it adds to the rebound after a sharp fall measured against its 60-day volatility.
- `031-01.g1.b2.g2_wide-range-day-rebound` (from F5, F7): The wider a coin's day range compared with its own daily volatility over the past 60 days, the more it rises above its normal drift over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
