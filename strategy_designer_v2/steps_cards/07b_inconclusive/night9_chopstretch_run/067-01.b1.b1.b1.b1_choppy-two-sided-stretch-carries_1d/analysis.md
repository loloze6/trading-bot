---
line: 7.b inconclusive
backtest: 067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries_1d
idea tested: 067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3905 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but far short of the bar. The slope of the 10-day unusual return on the forecast is +0.00057 with a day-clustered t of 0.73 (408 cases, 187 days). In folds B and C alone it is again positive and short: slope +0.0018, t 1.12 (143 cases, 73 days), and +0.0016, t 1.79 at 5 days (287 cases, 150 days).
- **F2:** The effect is mixed by side, which failed the supporting check. Over 10 days the short side's mean unusual move is +0.72 % and the long side's is −0.35 %. In folds B and C the shorts earn +3.3 % per case (strength 0.21, t 1.36, 77 cases) and the longs +0.7 % (strength 0.00, t 0.30, 66 cases). At 5 days the shorts earn +2.7 % (t 2.17, 145 cases) and the longs −0.2 % (t −0.16, 142 cases).
- **F3:** The effect is diluted rather than absent. Overall its size is −0.05 % per case, strength −0.016, t −0.09 over 536 days, against a usual 10-day move of 14.49 % and a trade cost of 0.19 %. Inside folds B and C, the 80 of 143 cases at 10 days whose 60-day return could not be read inside the window carry nothing: long strength −0.04, short +0.02. The 21 shorts whose 60-day return was below zero carry a strength of 0.59 (+9.6 %, t 2.24).
- **F4:** The carry differs from coin to coin. Over 10 days in folds B and C, XRP shows slope t 1.55, strength 0.20, BTC t 1.02, strength 0.13, and ZEC strength 0.29. ETH and LTC are negative (strength −0.08 and −0.05). Each coin has only 16 to 30 cases, so six coins cannot show an effect of this strength.
- **F5:** The grading along the stretch is uneven. At 10 days, the highest sixth of the forecast (mean +19.1) is followed by +4.1 % of unusual move. The lowest two sixths (mean −14.1 and −8.1) are followed by −3.1 % and −4.4 %. The four sixths between them, of both signs, sit near −0.7 % to −2.5 %. By year in folds B and C, the slope is −0.006 (t −4.2) in 2018 and positive in 2020 (t 0.96).

## Ideas
- `067-01.b1.b1.b1.b1.b1_choppy-stretch-carries-more-coins` (from F1, F3, F4): In a choppy market, a coin's close above or below its 20-day average, measured in units of its 20-day standard deviation of daily returns, is followed by a move the same way over the next 10 days. The further the close stands from the average on either side, the larger that move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
