---
line: 7.g patterns
backtest: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
idea tested: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5626 USD
---
## Findings
- **F1:** In choppy calm markets the effect runs opposite to the brief: price continues away from the middle of the range instead of returning to it. The excess return rises with the close's place in the 20-day range. Over 5 days the slope is +0.093 (day-clustered t 2.47, 104 cases on 49 days). Over 10 days it is +0.175 (t 2.53, 50 cases on 24 days). Over 5 days, closes in the upper half gain +4.10 % beyond drift (t 2.44, 57 cases) and closes in the lower half lose −3.70 % (t −2.68, 47 cases). Over 10 days, the top fifth gains +13.9 % (10 cases) and the middle fifth loses −7.0 % (14 cases).
- **F2:** In choppy agitated markets, closes in the lower half of the 20-day range are followed by falls. Over 5 days the excess is −7.57 % (t −3.36, 35 cases) against −2.56 % for the upper half (t −1.38, 13 cases). Over 10 days the bottom fifth falls −15.5 % (t −2.85, 8 cases). The graded slope on range position is weaker: +0.104 (clustered t 1.26, 48 cases on 38 days). The profile map has no strategy in the choppy agitated short box (0).
- **F3:** The continuation also holds in the rising calm profile, which agrees with the tested idea: 10-day slope +0.103 (clustered t 2.71, 119 cases on 37 days). It is absent in falling markets: falling calm −0.046 (t −0.52, 127 cases), falling agitated +0.044 (t 0.73, 82 cases).
- **F4:** The choppy calm continuation was not steady across years. Its 5-day slope was about 0 in 2018 (−0.004, t −0.08) and 2019 (+0.001, t 0.06), then +0.196 (t 1.96) in 2020 and +0.146 (t 2.92) in 2021. By coin it is carried mostly by XRP: +0.298 (t 3.76, 22 cases); the other measurable coins are positive with t below 2.
- **F5:** The book earns on its long side and loses on its short side. Its 499 long trades average +7.64 % net and its 221 short trades −4.29 % net, so the lower-half shorts trade against a coin's positive drift.
- **F6:** The book's gain sits in a few days. Its best 2 % of days (29 days, book +5.77 %, coins +5.46 %) carry 117 % of its summed daily gain. Its worst 2 % (book −4.40 %, coins −6.83 %) fall less than the coins.
- **F7:** The weekday pattern does not stand out against the many angles examined, so I propose no idea from it. Fridays and Saturdays look high: day-mean coin returns of +0.56 % (t 1.81) and +0.63 % (t 2.43). But the Friday-Saturday minus other-days gap fades by year: t 1.51 in 2018, 2.72 in 2019, 0.95 in 2020 and 0.10 in 2021.

## Ideas
- `058-02.b1.b2.b1.b2.b1.b1.g1_choppy-calm-edge-continuation` (from F1, F3, F4): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days, and the lower it sits, the larger its fall, with the move growing as the close nears an edge.
- `058-02.b1.b2.b1.b2.b1.b1.g2_choppy-agitated-low-continuation` (from F2, F5): In a choppy, agitated market, the lower a coin's close sits within its 20-day high-low range, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
