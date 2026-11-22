---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3602 USD
---
## Findings
- **F1:** The test's positive result comes from the largest quiet-volume rises only. Rises above 3 times the 30-day mean absolute hourly move, on volume 0.67–1.5 times its 30-day mean, give back 16.7 bp over 2 hours (t 2.15, 322 non-overlapping cases), 20.2 bp over 4 hours (t 1.50, 170) and 30.2 bp over 6 hours (t 1.37, 101), with strength 0.14 to 0.17. Quiet rises of 2–3 times give −4.8 bp (t −1.15, 834), and those of 1–2 times give +1.0 bp (t 0.44, 2,771).
- **F2:** The forecast flattens the grade the supporting slope needs. 32 % of short cells sit at |forecast| ≥ 19.9, and these hold rises of 0.69 to 12.6 times the usual move (mean 2.0). Cells with |forecast| 10–21 give only 1.1 bp (t 0.57, 3,897), while 5–10 gives 5.7 bp (t 1.48, 882). So the regression on |forecast| (slope −1.3e-05) cannot see the larger giveback of the largest rises.
- **F3:** Measured on the scaled rise itself instead of the clipped forecast, the grade is positive. Among quiet rises above 2 times, the slope over 2 hours is 11.1 bp per unit (t 2.31, 1,156 cases). Among rises above 1 times, the slope is 10.7 bp per unit over 4 hours (t 2.28, 2,019) and 14.6 bp per unit over 6 hours (t 1.97, 1,322).
- **F4:** The giveback of large quiet rises grows with the horizon and is larger in BTC. In BTC it is 15.9 bp over 2 hours (t 1.93, 143), 36.3 bp over 4 hours (t 2.08, 73) and 57.7 bp over 6 hours (t 2.47, 42, strength 0.33). In ETH it is 17.4, 8.1 and 10.6 bp (t 1.41, 0.41, 0.31). Over 4 hours it is positive in 7 of 8 years; 2024 is the exception at −40.6 bp (t −1.37, 27).
- **F5:** The effect is drowned in the tested measure by its many small cases. Over 2 hours, the forecast's cases total 0.03 % per case (strength 0.026), against a cost of 0.11 % per trade. The 6-hour giveback of rises above 3 times, 0.30 % (strength 0.17), is about 2.7 times that cost.
- **F6:** The opposite case is clear: large falls on surging volume rebound. Hours falling more than 3 times the usual move on volume above 3 times its 30-day mean are followed by a rise of 24.3 bp beyond drift over 2 hours (t −3.01 in the short-signed measure, 838 cases) and 24.9 bp over 4 hours (t −1.56, 432). This is against the brief's continuation, and on the coin's own bars.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade` (from F1, F2, F3, F4, F5): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next six hours. The larger that hour's rise in multiples of its typical move, the larger the giveback, most of all for rises several times the typical move.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins` (from F1, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two hours. The larger that hour's rise, the larger the giveback.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound` (from F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two hours. The larger that hour's fall, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
