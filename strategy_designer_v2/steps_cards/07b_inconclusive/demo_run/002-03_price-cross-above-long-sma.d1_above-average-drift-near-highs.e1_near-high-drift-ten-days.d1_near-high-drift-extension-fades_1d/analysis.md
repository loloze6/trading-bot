---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3379 USD
---
## Findings
- **F1:** The tested forecast has almost no link to the next 10 days on trending bars. Its slope t is 0.91 over 833 independent cases, and it stays as weak at other horizons: t 0.44 at 5 days (1674 cases) and t 0.65 at 20 days (408 cases).
- **F2:** The raw position of the close in its 20-day close range, unstandardised and without the extension penalty, clearly predicts the 10-day excess return on the same trending bars. Its slope is 0.067 with t 3.45 over 698 cases, and t 3.65 at 5 days over 1402 cases. Below the 200-day average it has no effect (t -0.41 at 10 days), so the effect sits where the idea places it.
- **F3:** On trending bars the effect is graded and lies mostly in the extremes of the range. Closes at the top of the 20-day range (mean position 0.98, 200 cases) were followed by a 10-day excess of +4.55%, closes at the bottom (mean 0.03, 86 cases) by -4.62%, and the middle quintiles by between -0.6% and +0.7%.
- **F4:** The forecast's construction loses this signal. Its two lowest quintiles on trending bars sit at -20, the clip, yet earn excess returns of +0.40% and -0.76%, while its top quintile earns +1.41%. The 60-bar standardisation and the cubed 30-day penalty crush the range information, so the test measured a distorted version of the effect.
- **F5:** The extension part only shows at the very top of the 30-day return. On trending bars the 10-day excess rises from -2.50% to +4.16% across the first four quintiles of the 30-day return (mean returns -17% to +26%), then drops to +0.02% in the top quintile (mean +71%).
- **F6:** The forecast's effect is mixed across periods and coins, not just small. By year, its slope t ranges from +2.23 in 2021 to -2.75 in 2024. By coin it is under 1.3 in absolute value everywhere, with BTC negative (t -1.28) and XRP the most positive (t 1.30).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b1_range-position-drift-above-average` (from F2, F3, F4): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade` (from F5): While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days, except at its very largest 30-day returns, where the larger that return, the smaller the rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins` (from F1, F6): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, except when its 30-day return is already extended, where the larger that 30-day return, the smaller the rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
