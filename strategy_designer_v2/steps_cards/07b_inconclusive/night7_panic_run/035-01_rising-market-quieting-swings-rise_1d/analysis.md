---
line: 7.b inconclusive
backtest: 035-01_rising-market-quieting-swings-rise_1d
idea tested: 035-01_rising-market-quieting-swings-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2281 USD
---
## Findings
- **F1:** On folds B and C, the plan's main measure is on the side the idea predicts but short of the bar: the forecast-weighted mean excess 3-day return is +1.08 % with t 1.81 (650 cases on 253 days); over all four folds step 5 found +0.24 % with t 0.61 (1,209 cases).
- **F2:** Inside the rising profile the ordering the idea predicts holds but is noisy: high-forecast cases +1.14 % (t 1.73, 325 cases), low-forecast cases +0.86 % (t 1.05, 325 cases) and widening-swing (forecast 0) cases −0.58 % (t −0.80, 587 cases); step 5's supporting difference was +0.41 % and passed.
- **F3:** The sign holds at every horizon tested, but no horizon clears it cleanly. Positive-forecast excess is +0.43 % over 1 day (t 2.02), +1.08 % over 3 days (t 1.81), +2.44 % over 5 days (t 2.19, 385 cases) and +3.87 % over 10 days (t 1.60). The forecast-0 group is negative at each of these horizons (−0.20 %, −0.58 %, −1.21 %, −3.07 %).
- **F4:** The effect is positive on all 6 coins: BTC +0.22 % (t 0.29), ETH +0.74 %, XRP +0.82 %, XMR +1.22 % (t 1.63), ZEC +1.27 %, LTC +2.64 % (t 1.68). Each coin has only about 93 to 137 cases, so none is significant on its own.
- **F5:** Across windows the effect is mixed: 5 of the 10 windows shown are positive and 5 negative, from w11 +3.13 % (t 2.54) to w7 −5.35 % (t −2.58). The market's own moves in a few windows drown a small per-case edge.
- **F6:** The trend's strength inside the rising profile does not locate the effect: weak trend +1.62 % (t 1.75), middle +0.50 % (t 0.44), strong +2.73 % (t 2.15), 100 cases each. No narrower condition is clearly where the effect lives.
- **F7:** Cost is not the obstacle; uncertainty is. The total move per case (+0.89 %) is 4.6 times the 0.19 % cost of a trade and the unusual move (+0.53 %) is 2.7 times it, but its t is 1.20 over 475 days, and the book's Sharpe is 0.77, 0.22 above holding.

## Ideas
- `035-01.b1_quieting-swings-more-coins` (from F1, F2, F4, F7): In a rising market, a coin rises over the next 3 days, more so the lower the standard deviation of its daily returns over the last 14 days compared with the standard deviation over the 90 days before them.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
