---
line: 7.b inconclusive
backtest: 031-02.b1.b2.b1_failed-rally-longer-horizon_1d
idea tested: 031-02.b1.b2.b1_failed-rally-longer-horizon
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4256 USD
---
## Findings
- **F1:** The tested measure averaged a short side that carries the effect with a long side that has none. The short cases (forecast below 0) give a product mean of +0.0326 with t 2.58 (58 cases, 26 days) and a drift-removed 40-day return of −7.0 % (t −1.45). The long cases (forecast above 0) are 286 of the 344 grid cases and give a product mean of +0.00006 with t 0.003 and a drift-removed return of +0.17 % (t 0.03). Pooled, they leave the inconclusive t of 0.36.
- **F2:** The long side comes from the plan's +10 offset, which makes the forecast long whenever the close is farther from the yearly low than usual. The idea never predicts a rise there. The long bins show no consistent sign: (0, 0.5] +19.3 % (t 1.35); (1, 2] −8.8 % (t −2.11, product t −2.11); (2, 20] +0.2 % (t 0.04, 238 cases).
- **F3:** Among the short cases the effect is graded, as the idea says. Cases with forecast ≤ −2 fall 13.0 % against drift over 40 days (t −2.90, 30 cases on 15 days, product t 2.84, strength −0.35, 70 % down). The most negative tercile (≤ −1.40) falls 12.0 % (t −2.44, 38 cases on 20 days). The mildest short tercile rises 2.5 % (t 0.29). The Spearman correlation of forecast with drift-removed return among short cases is +0.19.
- **F4:** The short-side fall shows at the idea's 40-day horizon and at longer horizons, but not at shorter ones. For forecast ≤ −2, drift-removed returns are −1.3 % at 10 days (t −0.52), +0.2 % at 30 days (t 0.01), −13.0 % at 40 days (t −2.90), −16.9 % at 50 days (t −1.42), −35.1 % at 70 days (t −2.01) and −48.1 % at 90 days (t −2.81, 10 cases).
- **F5:** The short-side fall is mixed across periods and coins, and its evidence rests on few days. By year: 2018 −17.4 %, 2021 −4.9 %, 2025 −16.3 % (t −1.97), but 2024 +2.7 %. By coin: XMR −13.4 % (t −3.09), ETH −15.2 %, INJ −28.9 % (t −2.94), but LINK +23.7 % and BTC +0.8 %. Window w12 holds 12 short cases on 3 days and w22 holds 6 cases on 1 day.
- **F6:** The short side is large against cost but not on enough days. Short cases with forecast ≤ −2 have a total 40-day move of −7.2 % in the short's favour, about 33 times the 0.22 % cost of a trade. The test already used all 19 coins and all four folds, so the only remedy is to measure the idea on its own side rather than on more data.

## Ideas
- `031-02.b1.b2.b1.b1_failed-rally-near-side` (from F1, F2, F3, F4, F6): The closer a coin's daily close is to its lowest close of the past 365 days, compared with how close it has usually been over that year, the more it falls over the next 40 days, while its 60-day return is positive, only while the close is nearer its yearly low than it has usually been.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
