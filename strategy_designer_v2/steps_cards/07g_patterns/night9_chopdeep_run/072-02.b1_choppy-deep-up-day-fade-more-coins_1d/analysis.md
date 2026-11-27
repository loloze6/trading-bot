---
line: 7.g patterns
backtest: 072-02.b1_choppy-deep-up-day-fade-more-coins_1d
idea tested: 072-02.b1_choppy-deep-up-day-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4313 USD
---
## Findings
- **F1:** The tested effect is confined to calm choppy markets. On choppy up days, each unit of depth below the 20-day high (in 20-day swing units) lowers the next-day excess return by 0.36 % in calm markets (t -3.01, 391 bars), against +0.13 % in agitated markets (t 0.57, 112 bars). Pooling the two, as the tested book did, dilutes the effect, consistent with its inconclusive t of -0.82.
- **F2:** In calm choppy markets the next-day excess return falls step by step across thirds of depth: +0.50 % in the shallowest third (t 1.67, 268 bars), -0.27 % in the middle third (t -1.38, 258 bars) and -0.72 % in the deepest third (t -2.03, 217 bars). The deepest-minus-shallowest spread is about -1.2 %, about 5 times the 0.22 % cost of a trade.
- **F3:** The same depth slope shows on calm days in every trend and disappears on agitated days. It is -0.21 % per unit in falling calm (t -3.76, 1141 bars) and -0.24 % in rising calm (t -2.44, 1286 bars), against +0.06 % in falling agitated (t 0.94) and -0.06 % in rising agitated (t -0.39). The calm-wide form repeats the held calm nearness-to-high book (035-01.b1). The falling-calm up-day form (slope -0.38 %, t -4.47, 542 bars) repeats the held falling still-down bounce fades (074 family). Neither is a discovery.
- **F4:** Across all choppy bars the depth effect is unstable over time, so the calm choppy effect must be checked for this on the held-out folds. By year, 2020 carries it (slope -0.96 %, t -3.80, 254 bars) while 2018, 2019 and 2021 sit near zero (t -0.31, 0.10, -1.39). By window the sign flips: w16 -1.94 % (t -2.98) and w14 -1.00 % (t -2.41), against w12 +0.32 % (t 2.32) and w17 +0.74 % (t 2.11).
- **F5:** Other angles showed nothing new beyond the map:

## Ideas
- `072-02.b1.g1_choppy-calm-deep-up-day-fade` (from F1, F2, F4): In a choppy, calm market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
