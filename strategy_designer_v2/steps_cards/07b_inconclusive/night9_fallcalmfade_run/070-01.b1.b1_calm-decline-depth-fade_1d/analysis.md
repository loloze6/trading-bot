---
line: 7.b inconclusive
backtest: 070-01.b1.b1_calm-decline-depth-fade_1d
idea tested: 070-01.b1.b1_calm-decline-depth-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3638 USD
---
## Findings
- **F1:** In folds B and C, the deepest quarter of runs carries the whole effect. Those runs lost an average 22.7 % before the up close. The next day they gave back +2.71 % beyond drift (t 3.99, 72 cases on 43 days). The three shallower quarters, which lost 3.3 %, 6.1 % and 11.3 % on average, gave +0.41 %, -0.02 % and +0.72 % (t 0.63, -0.05, 0.89).
- **F2:** Scaling the run's fall by the coin's 30-day daily swing gives the same picture. The top quarter, with runs about 5.3 swings deep, gave +2.82 % unusual next-day move (t 3.34, 38 days), +2.63 % total, and +2.90 % over two days (t 2.78). The other three quarters gave +0.13 % to +0.77 % with t at or below 1.40. The rank correlation of scaled depth with the next-day move is 0.25 (p 7e-5).
- **F3:** Over all cases the effect is weak against cost. The verdict's unusual move is +0.34 % (t 1.60, 391 days) and the total move is +0.22 %, which is 1.0 times the 0.22 % trade cost. The deep quarter's total move, about +2.6 %, is about 12 times that cost.
- **F4:** On the folds shown (B, C), the plan's own measure reaches +0.91 % with t 2.33 (290 cases, 158 days). The full-data t is 1.60, so folds A and D dilute it. The deep half of runs is positive on 7 of 10 coins: ETH +3.04 % (t 3.28), ADA +3.13 % (t 2.35), BTC +3.45 % (t 1.97), XMR +1.77 % and LTC +1.77 %. The ones that are not positive have 5 cases or fewer.
- **F5:** Run length tells the same story as depth, but less sharply. Runs of about 5 or more down days gave +1.97 % (t 3.75, 57 days); shorter runs gave +0.12 % to +0.83 % (t at most 1.26).
- **F6:** The test already used all 19 coins and folds A to D on daily bars, so no more data is available. The result is short of the bar because many shallow breaks with no giveback dilute it, not because there are too few cases.

## Ideas
- `070-01.b1.b1.b1_deep-calm-decline-relief-fade` (from F1, F2, F3, F5, F6): In a falling, calm market, a day that closes up after an unbroken run of down days is followed by a fall over the next day, but only after runs whose total fall is deep against the coin's usual daily swing. The more daily swings that run of down days took off the price, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
