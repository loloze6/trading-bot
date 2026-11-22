---
line: 7.b inconclusive
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
idea tested: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3526 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: the 70 short cases show a mean short-signed unusual move of +1.75 % over 5 days with t 1.54. The median is only +0.49 % and the hit rate 51 %, so a few larger falls carry the mean, which drops to +1.43 % without the top 3 cases.
- **F2:** The effect is mixed across coins and years, each with too few cases to show alone. By coin, ETH is +4.33 % (t 1.21, 14 cases) and LTC +3.78 % (t 1.39, 12), against XMR at +0.97 % (13) and ZEC at −0.79 % (16); XRP gave no case at all. By year, 2018, 2021, 2022 and 2025 are positive (2025 +5.59 %, t 2.40, 9 cases) while 2020, 2023 and 2024 are negative (2024 −1.68 %, 16 cases).
- **F3:** The effect shows in downtrends and is absent in uptrends. Cases where the coin's 60-day return was negative gave +2.97 % with t 2.17 over 48 cases; cases after a positive 60-day return gave −0.93 % with t −0.47 over 22.
- **F4:** The idea's grading by thinness is barely there. Across terciles of thinness the cases gave +1.57 % (low), +1.66 % (mid) and +2.00 % (high), all with t under 1.2, and the plan's Spearman is only 0.045.
- **F5:** Recomputed from prices, all failed 20-day breakouts together (321 cases) do not fall; they rise slightly more than usual (short-signed −1.19 % over 5 days, t −1.62; −2.66 % over 10 days, t −2.41). The heavy-volume quartile carries that rise (−4.29 %, t −2.01 over 5 days; −7.83 %, t −2.96 over 10 days) while the thinnest quartile is flat (+0.37 %, t 0.35). This supports the idea's consequence of refusing heavily traded failures.
- **F6:** Lengthening the horizon does not sharpen the test's own cases: the short-signed unusual move is −0.18 % (t −0.43) over 1 day, +1.29 % (t 1.36) over 3, +1.75 % (t 1.54) over 5 and +2.29 % (t 1.34) over 10, over 68–71 cases. The plan's 5-day horizon is where it reads best.

## Ideas
- `029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline.b1_thin-failed-breakouts-more-coins` (from F1, F2, F5, F6): When a coin closes above its prior 20-day high, reaches further above it within the next 3 days, and then closes back below the old high, the coin falls over the next 5 days, only when the breakout day's volume was low against its 20-day average volume, and the lower that volume ratio was, the larger the fall.
- `029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline.b2_thin-failed-breakout-downtrend` (from F3, F4, F5): When a coin closes above its prior 20-day high, reaches further above it within the next 3 days, and then closes back below the old high, the coin falls over the next 5 days, only while its 60-day return is negative, and the lower the breakout day's volume was against its 20-day average volume, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
