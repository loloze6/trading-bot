---
line: 7.b inconclusive
backtest: 058-02.b1_rising-calm-deep-dips-extend_1d
idea tested: 058-02.b1_rising-calm-deep-dips-extend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3653 USD
---
## Findings
- **F1:** Step 5's main slope is on the predicted side but small (slope 0.00057, day-clustered t 0.61, 396 cases on 194 days). In folds B and C the same slope on the plan's standardised forecast is still weak (t 1.23, 226 cases, 99 days). On the idea's own scaled pullback, (close − 5-day closing high) / high / 30-day swing, it reaches t 2.67 over 5 days (200 cases, 88 days) and t 2.27 over 10 days.
- **F2:** The standardisation in the plan blurs the depth the idea grades. The forecast's deepest tercile sits at the −20 cap (mean −19.57) and spans raw depths that differ widely. This explains why the forecast's slope is weaker than the raw one even though the two correlate at 0.92.
- **F3:** The effect is not graded evenly. It sits in the deepest pullbacks. In rising calm markets, B and C, the 5-day excess return by depth quartile is −3.50 % for the deepest (mean depth −1.97 swings, t −2.87, n 50, 70 % negative). The other quartiles are +0.47 %, +3.36 % and +2.82 %, so shallow dips do recover as the brief expected.
- **F4:** The deepest-quartile fall comes from early years. It is −10.4 % in 2018 (7 cases) and −8.4 % in 2019 (12 cases), but +0.08 % in 2020 (22) and −0.37 % in 2021 (9). The per-year slopes run from t 0.36 to t 1.88, so no single period shows the effect clearly.
- **F5:** The coins point the same way but weakly. The per-coin 5-day slopes are all positive, with t from 0.51 (BTC) to 2.28 (ETH), on only 24 to 48 cases each. The deeper half falls short of the shallower half in ETH (−1.73 % vs +4.11 %), LTC (−2.47 % vs +7.19 %), XMR and ZEC, but not in BTC (+0.15 % vs −1.11 %) or XRP. Six coins give too few cases per coin to show it.
- **F6:** Across all folds the size is small and unsure. The unusual move in the short direction is −0.44 % per case (t −0.77, 413 days, strength −0.044 of a 10.60 % usual move), against a cost of 0.19 % per trade. The average signal is drowned by the shallow pullbacks, which rise, and by the rising-calm drift (+3.54 % excess at the 5-day high, n 84).
- **F7:** Outside rising calm the same slope is weaker (t 1.68 over 5 days, 856 cases). Most of the signal, such as it is, lives in the idea's profile.

## Ideas
- `058-02.b1.b1_deep-calm-uptrend-dips-extend` (from F1, F3, F5, F6): In a rising, calm market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
