---
line: 7.b inconclusive
backtest: 049-02_wide-day-high-close-giveback_1d
idea tested: 049-02_wide-day-high-close-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2279 USD
---
## Findings
- **F1:** Step 5's slope points the way the idea predicts but falls short of the bar (+0.000412, day-clustered t 1.73, 2877 days); in folds B and C the slope on the forecast is +0.00088 (t 2.07, 7321 bars), and it is positive in every year (2018 t 1.32, 2019 t 1.51, 2020 t 1.48, 2021 t 0.29), so the effect is steady but small rather than absent.
- **F2:** The lean shows in five of the six coins (XMR slope +0.00188 t 3.47, LTC +0.00148 t 2.54, ETH +0.00110 t 2.19, BTC +0.00074 t 1.62, ZEC +0.00072 t 1.26) and runs the other way only in XRP (−0.00094, t −0.95), so it is broad but weak on any one coin, and more coins would add cases.
- **F3:** The effect is concentrated in falling, agitated markets (slope +0.00456, t 3.49, 805 bars), and also shows in choppy agitated ones (+0.00364, t 2.69, 224 bars); it is about zero in rising markets (calm −0.00063 t −0.78, agitated −0.00065 t −0.59) and in falling calm ones (−0.00025, t −0.27).
- **F4:** The reversal grows with the day's width. On days in the widest fifth, the slope on (0.5 − close location) × width is +0.0126 (t 2.58, 1464 bars), and a close in the lowest fifth of the range is followed by +1.44 % next-day excess (t 4.73). The high-close side the idea names is weaker: −0.39 % (t −1.13) on the widest days.
- **F5:** Per case the total move is +0.15 % against a trade cost of 0.19 % (0.8 times), and the unusual move is 0.038 of a usual move (t 1.62, 2249 days), so the book lost money (Sharpe −0.29) on an effect too small to show clearly at six coins.

## Ideas
- `049-02.b1_wide-day-giveback-all-coins` (from F1, F2, F5): The higher a coin closes in its day's high-low range, and the wider that day's range is against the coin's usual daily range over the past 30 days, the larger its fall over the next day.
- `049-02.b2_falling-agitated-wide-day-giveback` (from F3, F4): In a falling, agitated market, the higher a coin closes in its day's high-low range, and the wider that day's range is against the coin's usual daily range over the past 30 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
