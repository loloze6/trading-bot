---
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
idea tested: N2-04_slow-and-fast-momentum
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3522 USD
---
## Findings
- **F1:** The book's gain is mostly timing and not the market's rise: of the 0.000804 mean daily gain before fees, the coin's drift × allocation explains 0.000252 and timing explains 0.000553 (t 3.64). The book is in the market on only 29–38% of days per coin. The coins' next-day return is 0.002937 on in-market days against 0.000311 on flat days (Welch t 3.21).
- **F2:** The edge sits in calm uptrends. The low-volatility tercile carries 47.6% of the summed position gain. Among both-returns-up grid bars, the 20-bar excess return is 0.0589 (t 2.11, n 44) in low volatility, 0.0347 (t 0.96, n 55) in mid and 0.0030 (t 0.06, n 42) in high. The vol-scaled next-day return while active falls from 0.125 (t 3.29) in low volatility to 0.059 (t 2.41) in high.
- **F3:** The idea as tested was not shown. Both-up bars give a 20-bar excess of 0.0328 (t 1.50, n 141), and r60 quintiles are not monotone: 0.0209, 0.0003 and 0.0268 for the upper three, with t at most 0.80. The only strong cell is a negative one in the second-lowest r60 quintile: -0.0566, t -3.02.
- **F4:** Within active days, the next-day coin return grows with signal size. By forecast quartile (mean forecast 4.0, 9.6, 13.9, 19.0), the next-day return is 0.00181, 0.00276, 0.00405 and 0.00458, and the position gain is 0.00049, 0.00129, 0.00314 and 0.00486.
- **F5:** The gain is not one coin but is uneven in time and trades.
- **F6:** The book earns less than holding but with far less risk. Its mean daily return is 0.000754 against 0.001208 for holding, and its Sharpe is 1.05 against 0.57. In falling years it nearly sidesteps the losses: 2018 is -0.00019 against -0.00331, and 2022 is -0.00032 against -0.00178.

## Ideas
- `N2-04_slow-and-fast-momentum.e1_calm-uptrends-persist-longer` (from F1, F2, F3): When a coin's slow and medium returns are both up, the move over the following weeks is larger the calmer the coin's recent daily moves have been; a quiet uptrend persists, a violent one does not.
- `N2-04_slow-and-fast-momentum.e2_unusual-momentum-strength-pays` (from F1, F4): While a coin is in an uptrend, the next day's return is larger the further its recent returns stand above their own usual size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
