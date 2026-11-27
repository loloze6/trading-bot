---
line: 7.g patterns
backtest: 070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d
idea tested: 070-01.g1.d2.d2_falling-market-depth-run-break-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4099 USD
---
## Findings
- **F1:** In a falling 60-day trend, the day after an up day that ends a down run moved −1.14 % beyond drift (556 cases, 191 days, t −2.80). In a rising trend it moved +0.36 % (447 cases, t 0.98) and in a choppy trend −0.60 % (183 cases, t −1.39). The fade lives in the falling trend only.
- **F2:** In a falling trend, the prior day's direction is what matters. Up days after a down day were followed by −0.76 %, −1.24 %, −1.02 % and −1.57 % across the four quartiles of the up day's size in 30-day swings (t −1.16 to −2.34, 129 to 145 cases each). Up days after an up day were followed by +0.20 %, +0.41 %, +0.32 % and −0.22 % (all |t| < 0.9).
- **F3:** Within falling-trend run breaks, the next-day move grows with the size of the up day itself. By tercile of the up day's return it was −0.82 % (t −1.46, 185 cases), −1.14 % (t −2.13, 186 cases) and −1.47 % (t −2.44, 185 cases). The linear slope on the up day's swing-scaled size is weaker: −0.0053 per unit, t −1.49, 556 cases.
- **F4:** The run's length does not grade the fade monotonically. Runs of 1, 2, 3 and 4+ down days gave −0.93 % (t −1.68, 281 cases), −1.52 % (t −2.15), −0.32 % (t −0.37) and −2.44 % (t −2.67, 54 cases). The run's loss (step 5 slope t −7.62) carries the grading better than its count.
- **F5:** The effect is one day long. Over two days on a non-overlapping grid, falling-trend breaks moved −0.90 % beyond drift (544 cases, t −1.48), less than twice the one-day −1.14 %.
- **F6:** All six coins show the falling-trend break fade with the same sign: from −0.96 % (XRP, t −2.16) to −1.57 % (ETH, t −3.05), with 74 to 106 cases each. Short-term volatility does not order it: −1.16 % (t −2.17), −0.37 % (t −0.74) and −1.67 % (t −2.45) by tercile of 20-day swing.
- **F7:** The book fails for its size, not for its edge. The unusual move per case is +0.55 %, 2.9 times the 0.19 % trade cost. But the book was in a position on only 22.5 % of falling-trend days, with a mean allocation of −0.186 (median −0.18, at most −0.51). That gives a daily standard deviation of 0.188 % and a mean of 0.0228 % on days in a position.
- **F8:** Other angles showed nothing that stands out after this many cuts:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `070-01.g1.d2.d2.g1_falling-bounce-size-fade` (from F1, F2, F3, F6): In a falling market, an up day that follows a down day is followed by a fall over the next day, and that fall is larger the larger the up day's rise against the coin's usual daily swing over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
