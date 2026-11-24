---
line: 7.b inconclusive
backtest: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d
idea tested: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4428 USD
---
## Findings
- **F1:** The tested short side holds at 3 days but is too weak to show. In my recomputation, wide (≥1.5× the 20-day mean range) days closing in the top quarter after a 5-day fall have a mean short unusual move of +1.06 % (t 1.34, 535 cases on 227 days). Step 5 measured +0.56 % with t 0.76. The edge fades with the horizon: +0.74 % at 5 days (t 0.59) and −0.46 % at 10 days (t −0.29).
- **F2:** The short-side effect differs by coin and by year rather than holding everywhere. It is positive in XRP (+2.98 %, t 2.50), XMR (+2.58 %, t 2.31), AVAX (+4.04 %, t 2.16) and SUI (+3.69 %, t 2.12). It is negative in ZEC (−2.79 %, t −1.59), UNI (−2.74 %, t −1.03) and AAVE (−1.79 %, t −1.00). By year it is +3.03 % in 2022 and +3.05 % in 2025, but −2.18 % in 2021 and −1.97 % in 2024.
- **F3:** The short side is not graded by width. Across the range-multiple quartiles the 3-day short move is +0.75 %, +0.06 %, +1.47 % and +1.96 %, none with t above 1.64. The slope of the coin's unusual rise on the range multiple in these cases is −0.0018 at 3 days and −0.0107 at 5 days. Only the deepest quarter of prior 5-day falls stands out, at +2.93 % with t 1.77 on 57 days, which is not clear enough to restrict the idea to.
- **F4:** The same wide, high-closing day without a prior 5-day fall is followed by a further rise, clearly and growing with the horizon. The unusual rise is +1.58 % over 3 days (t 2.61, 789 cases, 426 days), +2.23 % over 5 days (t 3.17, 396 days) and +4.52 % over 10 days (t 3.28, 337 days).
- **F5:** That rise after no prior fall is graded by the day's width. At 5 days the range-multiple quartiles give +0.37 %, +2.00 %, +2.65 % and +3.90 % (t 0.38, 1.83, 2.29, 2.25), with a slope of +0.024 per unit of multiple. The strength goes from 0.03 to 0.24 of the coin's usual 5-day move.
- **F6:** The continuation after no prior fall is stronger when the 60-day return is positive: +2.90 % (t 2.69, 206 days) against +1.59 % (t 1.86) when it is negative. It is not steady across years: t above 2 in 2020 (+4.33 %), 2021 (+6.36 %) and 2024 (+2.97 %), but negative in 2022 (−0.96 %) and 2025 (−0.97 %).
- **F7:** Pooled over both contexts, the move after such days is upward. At 10 days the unusual rise is +2.72 % (t 2.40, 495 days). So the short bet sits against the dominant reaction to a wide day closing at its high. That move is about 12 times the 0.22 % cost of a trade, where the tested short's 3-day total move was only 0.4 times it.

## Ideas
- `031-02.b1.b1.b1.d2.g1.b1_wide-high-close-day-continuation` (from F4, F5, F7): After a coin has not fallen over the past 5 days, a day whose range is wide against its average daily range over the past 20 days and which closes near its high is followed by a further rise over the next 5 days; the wider that day's range, the larger the rise.
- `031-02.b1.b1.b1.d2.g1.b2_uptrend-wide-day-breakout-continuation` (from F4, F5, F6): After a coin has risen over the past 60 days and has not fallen over the past 5 days, a day whose range is wide against its average daily range over the past 20 days and which closes near its high is followed by a further rise over the next 10 days; the wider that day's range, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
