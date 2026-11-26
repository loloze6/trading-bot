---
line: 7.g patterns
backtest: 059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d
idea tested: 059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4524 USD
---
## Findings
- **F1:** Over the grid of 7-day returns in folds B and C (1,063 non-overlapping cases), the coin's next 7-day excess return follows its own 30-day return in steps: -1.88 % (t -2.10, 234 cases) after a 30-day fall beyond 20 %, -1.80 % (t -1.70) after a fall of 5 to 20 %, -0.59 % when flat, +1.75 % (t 1.42) after a rise of 5 to 20 % and +1.83 % (t 1.76, 268 cases) after a rise beyond 20 %.
- **F2:** This 30-day continuation is steepest in a choppy market (60-day return within ±10 %), with day-clustered t. The next 7-day excess return is -11.4 % (t -2.06, 19 cases) after a 30-day fall beyond 20 %, -4.3 % (t -1.50) after a fall of 5 to 20 %, -0.5 % when flat, +5.3 % (t 1.54) after a rise of 5 to 20 % and +8.2 % (t 1.75, 14 cases) after a rise beyond 20 %; the falling and rising markets show no such clean order.
- **F3:** Inside the tested profile, the 30-day return carries more than the scaled week does. Grid cases with a 30-day rise (regime trending) have an excess return of +2.81 % (t 1.85, 79 cases) and those with a 30-day fall (unknown) -1.50 % (t -1.20, 69 cases). The tested scaled-week buckets are not ordered: -5.0 % (t -2.65) for a small rise, +6.8 % (t 2.22) for a mid rise and +2.8 % (t 1.29) for a large rise.
- **F4:** A 30-day fall beyond 20 % continues over the next 7 days mainly when the coin is calm (30-day swing at or below its median): -4.18 % (t -2.27, 69 cases on 32 days), against -0.92 % (t -0.40, 165 cases) when agitated. By year it is carried by 2021 (-5.04 %, t -2.37); 2018 to 2020 are near 0, so it is fragile.
- **F5:** The next-day rebound after a scaled one-day fall is graded (Spearman rho 0.114, p 3e-7 when agitated; 0.088, p 1e-4 when calm) and largest when agitated (+2.33 % after a fall beyond 1.5 daily swings, t 2.82, 86 days). In a falling agitated market it gives +1.32 % (t 2.24). That cell is already the most held on the profile map (13 strategies), so it is not a discovery.
- **F6:** I found no pattern by weekday that holds. Wednesday's next-day excess return of -0.49 % (t -2.80) appears in 2019 only (t -2.71), and the other years range from t -0.79 to +0.02.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.b1.b1.d1.b1.b2.d2.g1_choppy-month-move-continues` (from F1, F2, F3): In a choppy market, a coin's return over the next 7 days follows the direction of its return over the past 30 days, and the larger that 30-day move, the larger the move that follows the same way, both after rises and after falls.
- `059-01.b1.b1.d1.b1.b2.d2.g2_calm-month-fall-continues` (from F4, F1): In a calm market, the larger a coin's fall over the past 30 days, the larger its further fall over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
