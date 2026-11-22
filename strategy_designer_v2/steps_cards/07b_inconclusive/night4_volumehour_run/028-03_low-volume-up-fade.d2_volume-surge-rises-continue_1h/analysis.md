---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
idea tested: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3828 USD
---
## Findings
- **F1:** The tested forecast does not single out real surges, so its 8827 cases are mostly ordinary hours: bars with the smallest long forecast (0 to 1, n = 18630) show a 6-hour unusual move of −3.22 bp (t −2.27), and bars with the strongest forecast (10 to 20, n = 6165) show +0.11 bp (t 0.03), which is why the main measure sits at +0.36 bp with t 0.14.
- **F2:** Hours that actually match the idea's situation do continue, and the volume surge is what separates them: up hours of at least 3 thirty-day standard deviations on at least 1.5 times the 30-day mean volume are followed by a 24-hour unusual move of +61.56 bp (t 3.41, 829 independent cases, strength 0.147), while the same rises on ordinary volume give +6.47 bp (t 0.13, 65 cases, strength 0.002).
- **F3:** The continuation shows over a day rather than over the plan's six hours: up hours of at least 2.5 standard deviations on at least 3 times the mean volume give +21.74 bp at 6 hours (t 2.30, n 964, strength 0.109), +24.94 bp at 12 hours (t 1.90) and +59.57 bp at 24 hours (t 3.27, n 792, strength 0.142); for rises of at least 3 standard deviations the figures are +20.15 bp (t 1.82) at 6 hours and +72.58 bp (t 3.47, strength 0.178) at 24 hours.
- **F4:** The move is graded by volume, as the idea says: among up hours of at least 2.5 standard deviations, the Spearman correlation of the log volume ratio with the 24-hour unusual move is 0.063 (p 0.022, n 1318), and the volume quartiles from lowest to highest give −4.77, +27.70, +65.42 and +69.59 bp. The size of the rise itself grades the move less: its correlation is 0.040 (p 0.15).
- **F5:** The effect is uneven across coins and periods. For surging rises of at least 2.5 standard deviations on at least 2 times the mean volume, the 24-hour move is +122.74 bp for ETH in 2018–2021 (t 3.07) against +5.77 bp for BTC (t 0.20). In 2022–2025 it is +39.92 bp for BTC (t 1.79) and +36.37 bp for ETH (t 1.20). By year, surging rises gain at 24 hours in 2021 (+265 bp, t 3.74), 2023 (+101 bp, t 2.75) and 2024 (+82.7 bp, t 2.22), but lose in 2019 (−86.5 bp, t −1.50).
- **F6:** At 24 hours the unusual move of surging rises, about 0.60 % to 0.73 % per case (F2, F3), is 5 to 7 times the 0.11 % cost of a trade. At the plan's six hours it is 0.20 % to 0.22 %, about 2 times the cost. As tested, the move was 0.0 times the cost.

## Ideas
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day` (from F1, F2, F3, F4, F6): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The higher that hour's volume against its 30-day average, the larger the further rise.
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b2_larger-surge-rises-carry-further` (from F2, F3, F5): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise against its typical 30-day hourly move, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
