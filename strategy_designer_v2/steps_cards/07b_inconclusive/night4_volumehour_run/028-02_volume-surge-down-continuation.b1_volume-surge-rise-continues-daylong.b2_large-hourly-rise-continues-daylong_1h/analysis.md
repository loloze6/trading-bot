---
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3627 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar. The mean 24-hour excess return is +0.095 % with t 1.49 over 4,454 cases, a strength of 0.021 of a usual 4.12 % move, and the supporting check is essentially zero (+0.0000068). The rise is small and does not grow with the forecast.
- **F2:** The effect changes sign across years. Taking the first rising hour of at least 3 typical moves on above-average volume in each 24-hour cell, the 24-hour excess return is -0.59 % (t -1.53, 223 cases) in 2018 and -0.09 % in 2019. It is +1.03 % (t 3.13, 177) in 2021, +0.82 % (t 2.24, 194) in 2022, and only +0.10 % (t 0.43, 212) in 2025.
- **F3:** Both coins lean the predicted way on the same cases. ETH's 24-hour excess after such rises is +0.37 % (t 2.13, 873 cases) and BTC's is +0.16 % (t 1.23, 935). The weakness is one of size, not of one coin going against the idea.
- **F4:** The grading is not monotonic, which is why the supporting check is zero. On hours with volume at least 3 times the 30-day average, the 24-hour excess return depends on the size of the rise:
- **F5:** The sign depends on which hour of a cell is taken as the case. Taking instead the highest-volume rising hour of each 24-hour cell gives a negative 24-hour excess return at every volume level: -0.50 % (t -2.87, 394) at 1 to 2 times volume, -0.32 % (t -1.66, 389) at 3 to 5 times, and -0.24 % (t -0.53, 165) at 8 times or more. The effect is too small to survive a change of sampling.
- **F6:** Volume does not separate continuation from noise as the brief says. Rising hours of at least 3 typical moves on below-average volume are followed at 24 hours by +0.28 % (t 1.16, 206), against +0.12 % (t 0.91, 1,019) at 1 to 3 times volume.
- **F7:** The move per case covers the cost of a trade only together with the coin's drift. The total move is +0.24 %, 2.3 times the 0.11 % cost; the unusual move is +0.09 %, 0.9 times the cost.

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.b1_volume-rise-continues-six-coins` (from F1, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise measured in typical 30-day hourly moves, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
