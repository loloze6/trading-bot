---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d
idea tested: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5107 USD
---
## Findings
- **F1:** In the falling profile, the up days on which the coin is still down over 5 days are followed by a next day 1.19 % below the coin's normal drift (t −2.66, 598 cases on 191 days). The same kind of day in a rising market gives only −0.27 % (t −0.61, 401 cases), and up days with a positive 5-day return in the falling profile give −0.03 % (t −0.08, 698 cases). The fade belongs to a still-down bounce inside a falling market.
- **F2:** Among those falling still-down up days, the fade grows with the 5-day loss scaled by the 20-day swing. The deepest tercile gives −2.44 % (t −3.19, 196 cases on 71 days), the middle −1.13 % (t −2.00), the shallowest −0.05 % (t −0.09). This reproduces the tested idea's grading on folds B and C.
- **F3:** On the same falling still-down up days, the fade also grows with the width of the day's high-to-low range against its 20-day average. The narrowest tercile gives −0.25 % (t −0.41, 198 cases), the middle −1.53 % (t −2.85, 198 cases on 109 days), the widest −1.79 % (t −2.50, 202 cases on 88 days). Width is a second gradient the tested forecast does not use. Over all falling up days the same split gives +0.05 %, −0.88 % (t −2.49) and −1.02 % (t −2.09).
- **F4:** The book's ten deciles of gain per held bar show the same thing. The worst decile (mean −3.5 %) and the best (mean +6.6 %) both fall on the deepest scaled 5-day losses (z5 −2.47 and −3.04) and the widest days (range ratio 1.05 and 1.21). The middle deciles sit at z5 about −0.9 and a range ratio of about 0.73. The book's result is carried by deep, wide bounces.
- **F5:** The other angles gave nothing that stands out after this many cuts.

## Ideas
- `074-01.b1.b1.b1.b1.d1.d2.g1_wide-still-down-bounce-fade` (from F1, F3, F4): In a falling market, an up day on which the coin's 5-day return including that day is still negative is followed by a fall over the next day. The fall is larger the wider that day's high-to-low range is against the coin's average daily range over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
