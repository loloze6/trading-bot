---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3589 USD
---
## Findings
- **F1:** The book fails on its falls, not its gain: it makes 21.0% a year but its deepest fall is −50.6%, so Calmar is 0.42. Its deepest fall episode lasts 426 days across w1–w5 (−46.8%), and the second lasts 440 days across w12–w16 (−40.8%).
- **F2:** The book barely steps aside in its falls. On bars inside its three deepest falls, the coins' 20-day return averaged −1.5% (against +4.9% outside) and the close sat 26.7% below its 60-day high (against 18.7%). The book still held 0.46 of capital (against 0.52) and earned only 0.00018 a bar (against 0.00139).
- **F3:** Volume carries both the gain and the losses. The top volume-ratio quintile has the largest position (0.93) and gain (0.0041 a bar), but also the largest summed losses (−45.6 against −7.4 in the bottom quintile). Inside that quintile the gain is 0.00289 when the 20-day return is negative and 0.00493 when it is positive. The middle quintiles lose in downtrends (−0.00034, −0.00016) and earn in uptrends (0.00072, 0.00102).
- **F4:** The day's direction splits the volume effect over 7 days. In the top volume-ratio tercile, the excess 7-day return is +1.65% after an up day (t 2.18, 399 cases) and −1.01% after a down day (t −1.35, 319 cases). Thin volume after a down day is also followed by −1.51% (t −2.31, 324 cases).
- **F5:** High volume on down days gives only a short bounce. Next-day return after a top-quintile-volume down day is +0.92%, yet the excess over the next 7 days is −1.0%. So the large positions the book takes on heavy-volume selling days pay for one day and then give it back, while the book keeps them for the full week.
- **F6:** The book does best near the coin's high. Bars within 7% of the 60-day high carry the book's highest gain (0.0021 a bar, next-day return +0.25%). Bars more than 22% below it earn near nothing (−0.00002 to 0.0008).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d1_volume-surge-in-uptrends` (from F1, F2, F3): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only while the coin's own 20-day return is positive.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d2_volume-surge-on-up-days` (from F4, F5): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only on days the coin closed above its previous day's close.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d3_volume-surge-near-high` (from F2, F6): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only while the coin's close is near its 60-day high, with the effect growing the closer the close is to that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
