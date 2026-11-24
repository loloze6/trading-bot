---
line: 7.g patterns
backtest: 031-03.b1.b1.b1_aligned-20-day-continuation_1d
idea tested: 031-03.b1.b1.b1_aligned-20-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6011 USD
---
## Findings
- **F1:** The closer a coin's close sits to its highest high of the past 60 days, measured in units of its usual 20-day move, the higher its drift-removed 10-day return. On the full grid the bottom sextile (mean distance −3.11) earns −2.34 % and the top sextile (−0.22) earns +3.12 % (t 1.70, 76 days). Per tercile of the coin's 30-day volatility, the slope is +0.0281 with t 3.29 in the calmest third (589 cases, 97 days), +0.0224 with t 2.06 in the middle third (581 cases, 123 days), and −0.0004 with t −0.03 in the most volatile third (592 cases, 122 days).
- **F2:** The same calm-versus-volatile split holds for the tested 20-day signal. When the coin has risen over 20 days, the slope of the drift-removed 10-day return on the 20-day move is +0.0401 with t 2.40 in the calmest third (324 cases, 68 days), against +0.0063 (t 0.39) and +0.0106 (t 0.62) in the other two. In the top 20 % of 20-day moves, the calmest third earns +5.90 % (t 2.10, 132 cases) and the most volatile third +2.73 % (t 1.00).
- **F3:** The continuation is one-sided, toward rises. The top decile of 20-day moves (+2.5 usual moves) earns +4.19 % drift-removed and the next decile +4.82 % (t 1.65 and 1.77). The bottom decile earns −1.26 % (t −0.70). After 20-day falls the slope on the 20-day move is −0.0165 with t −0.78 (858 cases, 126 days). Aligned falls give +2.00 % in their direction with t 1.32, against +2.60 % with t 1.68 for aligned rises.
- **F4:** The 60-day alignment adds little that is distinct. The 20-day directional drift-removed return is +2.32 % with t 2.26 when the 60-day return agrees (1211 cases, 144 days), against +0.64 % with t 0.49 when it disagrees (551 cases, 117 days). The position of the close in its 60-day high-low range alone gives the same shape: top quintile +3.37 % with t 1.89, slope t 1.90.
- **F5:** The book's gains are not market exposure. Its daily returns correlate 0.03 with the coins' mean daily return. On its worst 2 % of days the book loses 6.16 % while the coins average −2.09 %. On its best 2 % of days it gains 6.43 % while the coins average −0.79 %. The yearly breakdown of aligned cases has a single negative year, 2022: −3.25 % with t −1.24.
- **F6:** I looked at more than 20 angles: weekday, the 1-day and 5-day moves, the volume ratio, volatility relative to its own 90 days, and the halves of the sample. Only F1 in calm coins clears t 3. The 1-day move, the 5-day agreement, the volume ratio and the weekday show nothing that stands out: all |t| < 2 or flat across groups.

## Ideas
- `031-03.b1.b1.b1.g1_calm-coins-near-highs-continue` (from F1, F2, F3): The closer a coin's daily close sits to its highest price of the past 60 days, relative to the size of its usual 20-day move, the more it rises over the next 10 days. This holds while the coin's 30-day volatility is in the lower part of its own range.
- `031-03.b1.b1.b1.g2_calm-upside-20-day-continuation` (from F2, F3, F4): The larger a coin's 20-day rise, relative to its usual 20-day move, the more it rises further over the next 10 days. This holds while its 30-day volatility is in the lower part of its own range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
