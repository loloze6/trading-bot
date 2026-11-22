---
line: 7.b inconclusive
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3531 USD
---
## Findings
- **F1:** The test's main measure is on the side the idea predicts, with t 2.28 over 759 cases. It stays inconclusive only because the supporting check fails: the upper |forecast| half earns 0.11 % less short excess than the lower half. My quartiles of the cases show no grading either: 0.97 % (t 1.66), 0.00 %, 0.66 %, 0.20 % from smallest to largest |forecast|.
- **F2:** The forecast multiplies two parts that grade in opposite directions. The weekend's fall size grades against continuation:
- **F3:** The other part, the weekend's hourly volatility against the prior week, grades the way the idea predicts:
- **F4:** The vol-ratio grading holds in both halves of the data, with the top-quartile short excess at +0.91 % (t 1.28) in 2018–2021 and +1.64 % (t 2.35) in 2022–2025. It is positive in all six coins (0.29 % for ZEC to 2.10 % for XRP). It is not stable by year: 2019 −0.54 %, 2020 −0.35 % and 2025 −1.56 % against 2022 +4.14 % and 2024 +3.76 % (t 4.73).
- **F5:** The same continuation after turbulent weekends shows after weekend rises, so it does not depend on the side:
- **F6:** The 48-hour horizon is where the effect shows. On the cases, the short excess is 0.09 % (t 0.39) at 24 hours, 0.46 % (t 1.51) at 48 hours and 0.36 % (t 0.94) at 72 hours. The plan's own size, an unusual move of 0.68 % per case, is 3.5 times the 0.19 % cost of a trade.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b1_turbulent-weekend-falls-continue` (from F1, F2, F3, F4, F6): When a coin falls over the weekend (Saturday 00:00 to Monday 00:00 UTC), it keeps falling over Monday and Tuesday. The fall is larger the more volatile the weekend's hours were compared with the coin's previous week, graded by that volatility comparison alone and not by the size of the weekend's fall.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction` (from F3, F5, F6): When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days. The continuation is larger the higher the weekend's volatility compared with the previous week.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
