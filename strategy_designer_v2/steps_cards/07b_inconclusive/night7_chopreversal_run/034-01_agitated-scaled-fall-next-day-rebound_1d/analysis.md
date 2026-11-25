---
line: 7.b inconclusive
backtest: 034-01_agitated-scaled-fall-next-day-rebound_1d
idea tested: 034-01_agitated-scaled-fall-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3433 USD
---
## Findings
- **F1:** In folds B and C, among agitated down days, the next-day excess return rises with the fall measured in 30-day swings, but only weakly: slope 0.0128, t 2.03 (1439 cases, 537 days); on the plan's own standardised forecast the slope is t 1.36. Step 5's pooled result is on the predicted side but short of the bar: slope 0.00049, t 1.89, 3753 cases, 1449 days. Its size is too uncertain to separate from zero: unusual move +0.34 % per case, t 1.67 over 1050 days.
- **F2:** The effect lives in falling agitated markets (60-day return below -10 %). There the slope is 0.0262 with t 3.04 (377 cases, 147 days). In choppy agitated markets it is 0.0074 (t 1.09, 704 cases) and in rising agitated markets 0.0002 (t 0.02, 358 cases). Pooling all three trends dilutes the effect, which is why the pooled t falls short.
- **F3:** Inside falling agitated markets the regain grows with the fall. The next-day excess return is +0.52 % in the smallest third of falls (mean 0.16 swings), +1.30 % in the middle third (0.60 swings) and +2.38 % in the largest third (1.45 swings). Even the middle third's regain is several times the 0.19 % cost of a trade.
- **F4:** The falling agitated slope is positive on all six coins: BTC 0.025 (t 4.26), ETH 0.034 (t 2.58), LTC 0.045 (t 3.65), XRP 0.032 (t 3.51), XMR 0.020 (t 1.87) and ZEC 0.011 (t 1.38). It is also positive in every window with enough cases (w14 0.021, w15 0.019, w16 0.035, w18 0.021), though w16 carries most of the certainty (t 7.69).
- **F5:** The same falls in calm falling markets show no regain: slope 0.0010, t 0.18 (622 cases). Rises in falling agitated markets do not reverse either: slope -0.0052, t -0.72. Both fit the brief's forced-selling asymmetry.
- **F6:** The regain is a one-day effect. Over three days, on a non-overlapping grid, the falling agitated slope is 0.0012 (t 0.06, 116 cases), so the test's one-day horizon is the right one.
- **F7:** Across all agitated falls the response is not linear. The quintile next-day excess returns are +0.67 %, +0.35 %, +0.43 %, +0.14 % and then +1.72 % in the largest fifth. The pooled slope rests mostly on the deepest falls.

## Ideas
- `034-01.b1_agitated-fall-rebound-more-coins` (from F1, F7): In an agitated market, the larger a coin's one-day fall measured against its 30-day daily swing, the larger its rise over the next day.
- `034-01.b2_falling-agitated-fall-rebound` (from F2, F3, F4, F5, F6): In a falling, agitated market, the larger a coin's one-day fall measured against its 30-day daily swing, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
