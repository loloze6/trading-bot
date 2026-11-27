---
line: 7.b inconclusive
backtest: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d
idea tested: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4306 USD
---
## Findings
- **F1:** The effect lives only in the deepest bounces: in folds B and C, for up-day closes in choppy markets, the deepest quarter of depths (−4.6 to −19 swings below the 20-day high, median −6.1) is followed by an unusual 10-day fall of +9.9 % in the short direction (t 4.35, 44 cases on 34 days, strength 0.44); the third and shallowest quarters see rises instead (−10.6 % and −11.3 %, strength −0.26 and −0.31).
- **F2:** The grading holds across the whole range of depth, but it crosses zero partway down rather than starting from nothing at the high. By eighths of depth, the unusual 10-day move in the short direction runs +12.6 % (t 4.80), +7.1 % (t 2.14), then about +0.3 % to +2.6 % in the middle eighths, and −10.0 % (t −2.00) in the shallowest eighth. The Spearman correlation of depth with the move is −0.31 (−0.32 without DOGE). A short sized on every bounce below the high therefore takes on the shallow bounces that rise, and these dilute the test's mean to +0.93 % (t 1.37).
- **F3:** The shallow bounces are what tie the test to the market's own swings, while the deep ones hold in every year. The shallowest quarter's unusual 10-day move in the short direction swings with the year: +18.7 % in 2018 and +11.3 % in 2019, then −6.4 % in 2020 and −27.6 % in 2021 (t −2.11). The deepest quarter stays positive in every year: +6.0 %, +7.3 % (t 4.30), +5.4 % and +13.9 % (t 5.01). By coin, the deepest quarter is positive on all 11 coins with cases (80 % of cases positive without DOGE).
- **F4:** The deep end of the effect does not depend on the up day, as the brief's theory says. Over 5 days, the deepest quarter falls by +5.8 % unusual after down days (t 2.15, 62 cases) and by +5.1 % after up days (t 3.63, 66 cases). Over 10 days, deep down days give +5.8 % (t 1.65) against shallow −6.9 %.
- **F5:** The deep-quarter effect shows in both halves of the choppy band: +7.8 % (t 2.94, 32 cases) when the 60-day trend is negative and +15.2 % (t 4.09, 12 cases) when it is positive. It is not confined to one side of the choppy band, so no narrower profile is supported.

## Ideas
- `072-03.b1.b1.d2.b1_deepest-bounce-below-high-fades` (from F1, F2, F3, F5): In a choppy market, on a day that closed up, among the bounces that close many daily swings below the 20-day high (in units of the coin's 20-day daily-return standard deviation, not against its own recent depths), the further below the high the close sits, the larger the coin's fall over the next 10 days.
- `072-03.b1.b1.d2.b2_deep-close-below-high-continues` (from F1, F4): In a choppy market, among days that close many daily swings below the coin's 20-day high (in units of its 20-day daily-return standard deviation), whether the day closed up or down, the further below the high the close sits, the larger the coin's fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
