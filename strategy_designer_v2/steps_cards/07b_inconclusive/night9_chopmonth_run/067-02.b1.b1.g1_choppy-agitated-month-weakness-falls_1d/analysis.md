---
line: 7.b inconclusive
backtest: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls_1d
idea tested: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3842 USD
---
## Findings
- **F1:** In folds B and C, inside choppy agitated, the 7-day short-side excess return on the non-overlapping grid is +8.7 % per case with a day-clustered t of 2.29, but on only 36 cases over 21 days. Step 5's full-fold measure is +0.70 % with t 0.59 over 133 days, so folds A and D must hold a much weaker or opposite effect that dilutes it to an unclear result.
- **F2:** The effect sits on the monthly-fall side. After a negative 30-day return the short excess is +9.4 % (t 2.12, 30 cases, 16 days). After a positive 30-day return it is +5.3 % (t 1.35) on only 6 cases. The idea's claim that "even modest monthly rises are followed by declines" rests on almost no evidence.
- **F3:** Inside the profile the fall is graded by the month's weakness. By 30-day-return quintile, the 7-day excess goes from −15.2 % in the lowest quintile (mean month −34.7 %) to −5.2 % in the highest (mean month +23.2 %). The deeper half of forecasts earns +13.6 % short against +7.7 % for the shallower half, and the supporting check also passed on all folds (+1.38 %).
- **F4:** The effect is uneven across periods and depends on a few days. By window, the short excess ranges from +0.4 % (w15, 8 cases) and +3.2 % (w9) to +32.9 % (w16, 5 cases). By year it is +1.5 % in 2019 (14 cases), +21.6 % in 2020 and +8.6 % in 2021. This mixed, clustered effect is why the full sample's t stays below 2.
- **F5:** The effect does not extend to choppy calm. There, the 7-day short excess is −1.7 % (t −0.69, 89 cases, 38 days), and the 30-day return instead predicts continuation both ways: quintile excess runs from −5.0 % to +9.1 % (Spearman 0.35). The shorting effect is specific to the agitated case, and to monthly falls within it.
- **F6:** The test used every coin and all four folds available, so there is no more data to add. Per case, the total move is +0.03 % against a 0.22 % trade cost, because the coins' normal drift (−0.96 % in the short direction) cancels the +0.98 % unusual move. Only cases with a larger move, the deep monthly falls of F2 and F3, can carry a cost.

## Ideas
- `067-02.b1.b1.g1.b1_agitated-chop-monthly-fall-continues` (from F1, F2, F3, F4, F6): In a choppy, agitated market, the deeper a coin's fall over the past 30 days, the more it falls over the next 7 days, only after the month has closed lower.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
