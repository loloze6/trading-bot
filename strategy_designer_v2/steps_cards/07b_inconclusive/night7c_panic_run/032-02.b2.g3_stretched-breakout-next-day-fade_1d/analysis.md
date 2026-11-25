---
line: 7.b inconclusive
backtest: 032-02.b2.g3_stretched-breakout-next-day-fade_1d
idea tested: 032-02.b2.g3_stretched-breakout-next-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3196 USD
---
## Findings
- **F1:** Step 5's result sits on the wrong side of the idea rather than short of the bar: the slope's t is -0.61, but the mean unusual short move is -0.28 % over 782 cases, and in folds B and C coins rose after a close above the prior 30-day high (+0.33 % the next day beyond drift, t 0.90, 326 cases), so on average the fade loses.
- **F2:** The weak negative slope comes from the smallest breakouts, not from a larger fall after the most stretched ones: the smallest quarter of distances above the high rose +1.73 % the next day (t 2.68, 82 cases), while the second, third and largest quarters moved +0.58 % (t 0.98), -0.58 % (t -0.84) and -0.44 % (t -0.48), so the next-day fall the idea needs never shows clearly.
- **F3:** Over longer horizons the move after a breakout runs the other way and grows with the stretch: the excess move was +1.06 % over 3 days (t 0.99, 97 cases), +5.12 % over 5 days (t 2.39, 54 cases) and +10.15 % over 10 days (t 2.50, 27 cases), and over 3 days a larger stretch was followed by a larger rise (slope +0.40, t 2.24, 97 cases).
- **F4:** The 1-day effect is not carried by any coin or year: by coin, the next-day excess moves range from -0.65 % (LTC, t -0.86) to +2.92 % (XRP, t 1.66), all with |t| < 2; by year, from -1.51 % (2018, t -0.79) to +0.63 % (2020, t 1.27), all with |t| < 2.
- **F5:** On the brief's own situation, a close below the prior 30-day low, a deeper break was followed by a larger next-day rise (slope +0.54 per unit of depth, t 9.16, 180 cases), and the rebound was concentrated where 20-day volatility ran above 1.2 times its 120-day level (+4.81 % next day, t 2.54, 28 cases, against +0.01 %, t 0.02, 152 cases elsewhere).

## Ideas
- `032-02.b2.g3.b1_stretched-breakout-multi-day-continuation` (from F1, F3): When a coin closes above its highest high of the prior 30 days, the further the close sits above that high, the more the coin rises over the next 3 days.
- `032-02.b2.g3.b2_agitated-monthly-low-rebound` (from F5): When a coin closes below its lowest low of the prior 30 days while its daily swings are wider than over the past months, the further the close sits below that low, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
