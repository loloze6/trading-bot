---
line: 7.b inconclusive
backtest: 072-01.b1.b1_choppy-deep-close-more-coins_1d
idea tested: 072-01.b1.b1_choppy-deep-close-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4035 USD
---
## Findings
- **F1:** The tested slope points the way the idea predicts but is short of the bar, and it does not hold across years. In folds B and C the 5-day grid gives 390 cases on 166 days, with a short-side slope t of 1.65 that falls to 1.35 when returns are winsorized. The deep tercile falls 2.9 % beyond drift (t 2.64), but by year the mean short gain is +6.4 % in 2018 (t 5.64), +1.8 % in 2019 (t 2.34), +0.8 % in 2020 (t 0.72) and −3.6 % in 2021 (t −1.05).
- **F2:** The gap between deep and shallow closes in the means comes mostly from a few extreme moves, not from a steady grade. The shallow tercile's 5-day mean is −3.1 %, pulled by one case of +385 % and five cases beyond ±30 %, while the tercile medians are nearly flat (shallow 1.3 %, mid 1.7 %, deep 1.6 %) and the Spearman rho of depth against the 5-day short return is only 0.06.
- **F3:** The depth grade appears only while the coin's last 5 days were down. After a negative 5-day return, the 5-day short gain rises from −1.1 % (shallow, n 14) to 1.6 % (mid, n 76, t 1.99) to 4.8 % (deep, n 94, t 3.56). After a positive 5-day return there is no grade: −3.6 % (shallow, n 112), 2.6 % (mid, n 51), −1.5 % (deep, n 33).
- **F4:** The 20-day return splits the cases the same way. The cases with a negative 20-day return gain 2.9 % to 3.8 % in every tercile (deep: n 99, t 2.74), while the shallow cases are mostly ones whose 20-day return was positive (97 of 130) and gain −4.8 %.
- **F5:** Measured at another horizon, the idea is not clearer. The 1-day slope t is 0.43 (2040 cases, 854 days), the 2-day slope t 0.75 and the 3-day slope t 0.95, so depth alone carries no next-day grade. Only the deep tercile after an up day falls next day (0.9 %, t 2.38), against −0.2 % after a down day.
- **F6:** The book's capture is too small to pay. Over 5 bars the unusual move per case is +0.45 % (t 1.35 on 1112 days), only 2.0 times the 0.22 % cost of a trade, and the total move is −0.34 % per case because the drift on the short side is −0.79 %. The book's Sharpe is −0.21.

## Ideas
- `072-01.b1.b1.b1_choppy-deep-close-falling-week` (from F3, F4, F2, F1): In a choppy market, the further a coin's close sits below its 20-day high, measured in units of the standard deviation of its daily returns over the last 20 days, the larger its fall over the next five days, only while its 5-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
