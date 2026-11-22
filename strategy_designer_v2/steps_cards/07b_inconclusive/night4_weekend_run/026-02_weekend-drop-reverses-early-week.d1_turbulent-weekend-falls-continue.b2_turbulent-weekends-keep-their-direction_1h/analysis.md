---
line: 7.b inconclusive
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.1356 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but just short of the bar: the mean unusual 48-hour move is +0.37 % per case with t 1.96 over 1,687 Monday cases, a strength of 0.052 of the coin's usual 6.56 % move, which is the usual size of a real idea.
- **F2:** The effect is not confined to some coins. It is positive in every one of the six: BTC +0.25 % (t 1.08, 282 cases), ETH +0.45 % (t 1.39, 282), LTC +0.37 % (t 0.98, 282), XMR +0.33 % (t 0.98, 279), XRP +0.46 % (t 0.88, 282) and ZEC +0.34 % (t 0.85, 280). The test is short of cases, not short of a part where the effect shows.
- **F3:** It is positive in every year, though weaker late: 2018 +0.59 % (t 1.25, 295 cases), 2019 +0.34 % (t 0.94, 308), 2020 +0.59 % (t 1.39, 314), 2021 +0.26 % (t 0.92, 311), 2022 +0.02 % (t 0.05, 301) and 2023 +0.00 % (t 0.01, 156). No single period carries it.
- **F4:** The horizon the plan chose is where the effect is clearest.
- **F5:** Neither one side nor the largest forecasts carry the effect.
- **F6:** Per case, the total move of +0.40 % is 2.1 times the 0.19 % cost of a trade. A clear answer on more cases is worth having, even though the book (Sharpe 0.73, mean daily return 0.028 %) fell short of the profitability bar.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.b1_turbulent-weekends-continue-more-coins` (from F1, F2, F3, F4, F5): When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days. The continuation is larger the higher the weekend's volatility compared with the previous week.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
