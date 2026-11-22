---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade_1h
idea tested: 028-03_low-volume-up-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3222 USD
---
## Findings
- **F1:** The test's own result is on the side the idea predicts but too small for this data to show clearly. Recomputed on 12,172 cases, the 6-hour giveback after the short bets, drift removed, is +0.020 % with t 1.12, against step 5's +0.022 % with t 1.21. It is the same sign on both coins: BTC +0.019 % (t 0.86, 6,276 cases) and ETH +0.021 % (t 0.74, 5,896 cases).
- **F2:** The giveback shows most clearly over the first two hours and fades after. It is +0.015 % (t 2.05) over 1 hour, +0.035 % (t 3.29) over 2 hours, +0.023 % (t 1.84) over 3 hours, +0.020 % (t 1.12) over 6 hours and +0.021 % (t 0.82) over 12 hours. The 2-hour reading holds on both coins: BTC +0.029 % (t 2.15) and ETH +0.054 % (t 3.13).
- **F3:** The effect is not graded by the size of the rise. The correlation of the hour's rise, in usual moves, with the next 2-hour giveback is -0.003, and with the 6-hour giveback also -0.003. Across |forecast| quintiles the 6-hour giveback goes +0.053 %, +0.005 %, +0.029 %, -0.034 %, +0.047 % with no trend. Rises of 2 to 3 usual moves show a 6-hour continuation of -0.062 % (t -1.22). Step 5's larger-half minus smaller-half difference is -0.0018 %.
- **F4:** The effect is mixed across years. The 6-hour giveback is +0.112 % (t 1.69) in 2018 and +0.068 % (t 1.62) in 2025. It is -0.101 % (t -2.03) in 2020 and -0.057 % (t -1.73) in 2023.
- **F5:** On the plain 6-hour grid, the market's own moves point the other way. Quiet-volume hours (0.5 to 1.5 times the 30-day mean) that rose 1 to 2 usual moves were followed by a further rise of +0.074 % over 6 hours, drift removed (t 1.39, 1,322 cases). Those rising 2 to 4 usual moves were followed by -0.009 % (t -0.11).
- **F6:** The idea is tiny next to the cost of a trade. Its unusual move is 0.011 of the coin's usual 6-hour move (1.98 %). Its total move is -0.01 % per case against a cost of 0.11 % per trade. Even the 2-hour giveback of +0.035 % is about a third of that cost.

## Ideas
- `028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider` (from F1, F4): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two to six hours. The larger that hour's rise, the larger the giveback.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade` (from F2, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next two hours. The larger that hour's rise, the larger the giveback.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
