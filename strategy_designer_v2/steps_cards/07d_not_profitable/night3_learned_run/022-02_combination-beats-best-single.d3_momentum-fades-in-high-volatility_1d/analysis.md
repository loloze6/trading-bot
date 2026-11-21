---
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
idea tested: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3268 USD
---
## Findings
- **F1:** The tested momentum does not predict the next 20 days. The rank correlation of the volatility-scaled 28-day return with the 20-day unusual move is 0.03, and its signed unusual move is -0.33 % per case (t -0.34, 539 cases). Its quintiles do not rise in order: -1.58 %, -1.45 %, +3.35 %, -1.67 %, +0.64 %. Its size, -0.44 % per case, is below zero, so no holding, sizing or threshold can bring it over the 0.19 % cost.
- **F2:** The volatility condition runs against the idea. In the calmest third of 30-day volatility against its own past, signed momentum lost 2.53 % per 20 days (t -1.25, 180 cases); the middle third gained 1.15 % (t 0.91) and the wildest third 1.19 % (t 0.73).
- **F3:** The momentum effect flips sign between periods. Signed 20-day unusual moves were +5.2 %, +3.4 % and +2.8 % in 2018, 2019 and 2020 (t 1.83, 1.78, 0.88; 66 to 72 cases each). They were -6.1 %, -4.1 % and -2.8 % in 2021, 2022 and 2023 (t -1.64, -1.92, -1.51), and about 0 in 2024 and 2025.
- **F4:** The book's short side destroys what its long side earns. Long bars summed +12.18 of gain before costs over 8198 bars, short bars -5.96 over 9124 bars. Short trades averaged -6.12 % net with 31 % winners (2146 trades), long trades +10.82 % net with 49 % winners (1506 trades).
- **F5:** The failing Calmar of 0.066 comes from a deep, long fall. The chained pooled book reached falls of -59 % to -65 % through windows 5 to 10, while its mean daily return there was between -0.0015 and +0.0026.
- **F6:** The book trails holding because it is short in rising years. In 2020 it earned 0.00103 a day against the coins' 0.00423, in 2021 0.00014 against 0.00409, and in 2023 it lost 0.00169 while the coins gained 0.00150 (overall mean 0.00032, below the 0.0005 floor).
- **F7:** Nearness to the 60-day high carries a 20-day move the momentum lacks. Cases closer than the coin's median to their 60-day high, against those farther, gave a signed unusual move of +3.59 % per 20 days (t 2.97, 395 cases), about 19 times the 0.19 % cost of a trade.

## Ideas
- `022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility.d1_nearness-to-60-day-high` (from F7, F4, F1): The closer a coin's close sits to its highest close of the past 60 days, the higher its return over the next 20 days.
- `022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility.d2_momentum-near-recent-highs` (from F7, F1, F2, F5): The higher a coin's 28-day return, the higher its return over the next 20 days, the more so the closer its close sits to its highest close of the past 60 days.
- `022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility.d3_long-side-momentum-after-rises` (from F4, F6, F5): The higher a coin's 28-day return, the higher its return over the next 20 days, only while that 28-day return is above zero, the more so the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
