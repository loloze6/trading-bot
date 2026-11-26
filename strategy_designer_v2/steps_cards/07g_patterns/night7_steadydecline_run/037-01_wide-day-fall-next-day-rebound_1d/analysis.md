---
line: 7.g patterns
backtest: 037-01_wide-day-fall-next-day-rebound_1d
idea tested: 037-01_wide-day-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3955 USD
---
## Findings
- **F1:** In folds B and C the next-day excess return after a down day grows with the fall and the width together. The coin's largest-third falls on its widest-third ranges are followed by +1.25 % (t 5.67, n 882). The same large falls on its narrowest-third ranges are followed by −0.24 % (t −0.28, n 81). Small falls on wide ranges are followed by −1.18 % (t −2.20, n 117), so width only pays when the fall is large.
- **F2:** The idea's gain sits in agitated markets. After the coin's largest-third falls, the next day's excess return is +1.27 % (t 4.28, n 603) in the coin's highest third of 20-day swing, +0.80 % (t 3.37, n 382) in its middle third, and −0.27 % (t −0.73, n 199) in its lowest third. On all bars with a positive forecast the split is the same: highest third +0.87 % (t 4.26, n 1190), lowest third −0.07 % (t −0.56, n 1206). On all bars, the swing level alone gives nothing (highest third +0.11 %, t 0.85).
- **F3:** The gain sits in the top of the forecast. Bars with a positive forecast in its highest third are followed by +0.75 % (t 4.57, n 1432), the middle third by +0.17 % (t 1.08), and the lowest third by −0.08 % (t −0.62). So the book pays the 0.19 % trade cost on many low-forecast days that earn nothing.
- **F4:** Among the largest-third falls, a close near the day's low rebounds more than a close near its high. A close in the bottom 20 % of the range is followed by +1.09 % (t 4.68, n 683), a mid-range close by +0.56 % (t 2.09, n 648), and a top-20 % close by +0.17 % (t 0.24, n 90).
- **F5:** The effect also holds over 3 days on the non-overlapping grid. Large falls on wide ranges are followed by +1.39 % excess over 3 days (t 2.15, n 258). Large falls on narrow ranges are followed by −1.13 % (t −0.35, n 26).
- **F6:** The edge is not steady across years and is concentrated in a few days. Bars with a positive forecast are followed by −0.19 % in 2018 (t −1.09) and +0.01 % in 2019, against +0.74 % (t 3.79) in 2020 and +0.68 % (t 3.52) in 2021. The best 5 % of non-zero book days sum to 2.4 times the book's total gain, which is consistent with the failed Calmar (0.69).
- **F7:** The next-day excess return also differs by weekday across all bars. It is +0.47 % after a Thursday bar (t 3.19, n 1242) and +0.39 % after a Friday bar (t 2.87), against −0.49 % after a Wednesday bar (t −2.69). This is a fixed calendar condition, not a graded situation, so no idea is drawn from it.

## Ideas
- `037-01.g1_wide-fall-rebound-agitated` (from F2, F1, F3): In an agitated market, the larger a coin's one-day fall and the wider that day's high-to-low range against its own average daily range over the past 14 days, taken together, the larger its rise over the next day.
- `037-01.g2_wide-fall-low-close` (from F4, F1, F3): The larger a coin's one-day fall, the wider that day's range against its average daily range over the past 14 days, and the nearer its close to the day's low, taken together, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
