---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
Consequence: A trader in a coin above its long average would lean long in proportion to how near the close is to its 20-day high, and stay out or light when it sits near its 20-day low.
Why:
- F2: The raw position of the close in its 20-day close range, unstandardised and without the extension penalty, clearly predicts the 10-day excess return on the same trending bars. Its slope is 0.067 with t 3.45 over 698 cases, and t 3.65 at 5 days over 1402 cases. Below the 200-day average it has no effect (t -0.41 at 10 days), so the effect sits where the idea places it.
- F3: On trending bars the effect is graded and lies mostly in the extremes of the range. Closes at the top of the 20-day range (mean position 0.98, 200 cases) were followed by a 10-day excess of +4.55%, closes at the bottom (mean 0.03, 86 cases) by -4.62%, and the middle quintiles by between -0.6% and +0.7%.
- F4: The forecast's construction loses this signal. Its two lowest quintiles on trending bars sit at -20, the clip, yet earn excess returns of +0.40% and -0.76%, while its top quintile earns +1.41%. The 60-bar standardisation and the cubed 30-day penalty crush the range information, so the test measured a distorted version of the effect.
