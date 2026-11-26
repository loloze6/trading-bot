---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days_1d
idea tested: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3745 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but stays short of the bar, because the small rises dilute it. At 5 days on folds B and C, the unusual move rises steadily across the quartiles of the one-day rise in 30-day standard deviations: -0.05 % (t -0.02, 43 days), +1.08 % (t 0.61, 47 days), +1.92 % (t 1.05, 43 days), +3.01 % (t 2.03, 37 days). Strength runs from 0.01 to 0.22, so the effect is carried by the largest rises.
- **F2:** The give-back shows most clearly over the next day. At 1 day the unusual move is +0.85 % (t 1.97, 235 days, 639 cases) with a strength of 0.157. Over 5 days it is +1.49 % (t 1.26, 121 days) with a strength of 0.118. The 1-day total move of +0.67 % is about 3 times the 0.22 % cost of a trade, while the tested 5-day total move is +0.00 %.
- **F3:** The effect varies by period, which keeps the pooled t low. At 5 days the unusual move is positive in 2018 (+1.62 %, t 0.57), 2019 (+2.13 %, t 2.55) and 2021 (+3.48 %, t 1.33), but negative in 2020 (-1.21 %, t -0.81). Windows range from -2.06 % (w17) to +4.52 % (w18).
- **F4:** The brief's own situation, a rise over several days, shows no give-back.
- **F5:** The tested idea already ran on all 19 coins and all four folds of daily data, so no more daily data is available to repeat it unchanged.

## Ideas
- `058-01.g2.b1.d3.b1_one-day-rise-fades-next-day` (from F2, F1, F4): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next day.
- `058-01.g2.b1.d3.b2_large-one-day-rises-fade` (from F1, F3, F4): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next 5 days, only when that rise is larger than the coin's usual daily swing over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
