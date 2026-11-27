---
line: 7.b inconclusive
backtest: 041-01.b1_rising-agitated-rise-continues_1d
idea tested: 041-01.b1_rising-agitated-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4335 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: the day-clustered slope t is +1.86 over 1273 cases on 758 days. The mean excess next-day return is −0.044 %, so the supporting check fails, and the size is an unusual move of +0.12 % per case (t 0.44 over 529 days, strength 0.030 of a usual 5.25 % move).
- **F2:** In the explore half, rising-agitated up days give a slope of z on the next-day excess return with t +1.35 (240 cases), but their mean excess is −0.43 % (t −1.0). The slope comes mostly from the smallest rises (z 0 to 0.5: −1.53 %, t −2.88, 111 cases); the largest rises sit only slightly above drift (z > 2: +0.94 %, t 0.48, 16 cases; top quartile +0.68 %, 60 cases).
- **F3:** The effect does not show at another horizon. On non-overlapping grids the slope of up days' excess return on z has a t of −0.01 at 2 days (98 cases), 0.15 at 3 days (81) and 0.56 at 5 days (49).
- **F4:** The effect is weak but not confined to one part of the data. The correlation of z with the next-day excess return on rising-agitated up days is positive on every coin (BCH 0.07, DOGE 0.15, ZEC 0.10) and in every year (2018 0.48, 2019 0.13, 2020 0.02, 2021 0.08), so no coin, year or band of forecasts carries it alone.
- **F5:** The brief's fall reversal is absent inside the profile but present outside it. Inside, rising-agitated down days show no rebound: the slope on z is +0.009 (t 1.15, 239 cases), so larger falls are followed by slightly lower next days. Outside the profile, scaled falls of z −2 to −1 rebound +1.65 % (t 3.12, 154 cases) and falls beyond −2 rebound +2.35 % (t 2.22, 34 cases).
- **F6:** The move is too small to pay at this cost. The total move per case is +0.23 % against a trade cost of 0.37 % (0.6 times), and the unusual move is 0.3 times the cost.

## Ideas
- `041-01.b1.b1_rise-continuation-more-coins` (from F1, F2, F4): In a rising, agitated market, the larger a coin's one-day rise measured against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
