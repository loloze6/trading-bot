---
line: 7.g patterns
backtest: 032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d
idea tested: 032-02.b2.g2.d1_near-low-rebound-in-falling-months
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3864 USD
---
## Findings
- **F1:** Across all bars of folds B and C, not only the tested regime, the lower the close sits in the day's high-low range, the higher the next-day excess return: the slope is +0.32 % per standard deviation of close location (t 2.90, 8688 bars, 1448 days); closes in the lowest fifth of the range are followed by +0.52 % (t 2.05) and closes in the highest fifth by −0.34 % (t −1.66).
- **F2:** This near-low rebound points the same way on every year and every coin: the yearly slopes run from +0.23 % to +0.61 % (t 1.06 to 2.70), and the coin slopes from +0.14 % for XRP (t 0.76) to +0.67 % for XMR (t 4.82).
- **F3:** The near-low rebound does not need the tested regime: outside it, closes in the lowest fifth of the range earn +0.37 % against −0.25 % for the highest fifth. It is stronger in down months, with a slope of +0.46 % (t 2.56, 775 days) when the 30-day return is negative against +0.26 % (t 1.97, 1118 days) when it is not.
- **F4:** The larger a day's fall relative to the coin's own 30-day daily volatility, the larger the next day's rise: the slope on the volatility-scaled day return is −0.40 % (t −2.38, 7537 bars, 1257 days), the most-fallen fifth of days is followed by +0.75 % excess (t 2.51, 446 days), and the effect is stronger in down months (slope −0.62 %, t −2.11) than otherwise (−0.28 %, t −1.46).
- **F5:** The volatility-scaled reversal also points the same way on every year (slopes −0.19 % to −0.68 %) and on 5 of 6 coins (ETH t −2.37, XMR −3.25, ZEC −2.69); XRP is flat (+0.01 %, t 0.03).
- **F6:** The near-low rebound sits mostly on down and flat days: its slope is +0.28 % (t 1.28) in the lowest tercile of the volatility-scaled day return and +0.33 % (t 2.06) in the middle one, but −0.11 % (t −0.61) in the highest.
- **F7:** The brief's own situation shows nothing: a new 30-day closing low is followed by +0.32 % next day (t 0.56, 226 days) and +0.21 % over 3 days (t 0.15, 67 days), and the tested regime's bars as a whole earn −0.06 % (t −0.18).
- **F8:** Both one-day effects are larger than a trade's cost of 0.19 %: +0.52 % after near-low closes and +0.75 % after the most-fallen fifth of days. Weekday, day-range level and the 30/90 range ratio show no group with |t| above 2, so the effect is in the shape of the day's move, not in the volatility regime.

## Ideas
- `032-02.b2.g2.d1.g1_near-low-close-rebounds-anywhere` (from F1, F2, F3, F7, F8): For any coin, in any market, the lower its daily close sits within that day's high-low range, the larger its rise over the next 1 day, and the more so when its 30-day return is negative.
- `032-02.b2.g2.d1.g2_volatility-scaled-one-day-fall-reversal` (from F4, F5, F8): The larger a coin's 1-day fall measured against its own daily volatility over the past 30 days, the larger its rise over the next 1 day.
- `032-02.b2.g2.d1.g3_down-day-close-at-low-rebounds` (from F1, F4, F6): When a coin closes the day lower than the day before, the nearer that close sits to the day's low, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
