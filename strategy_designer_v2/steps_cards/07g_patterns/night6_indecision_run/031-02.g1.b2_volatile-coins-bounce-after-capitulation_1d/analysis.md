---
line: 7.g patterns
backtest: 031-02.g1.b2_volatile-coins-bounce-after-capitulation_1d
idea tested: 031-02.g1.b2_volatile-coins-bounce-after-capitulation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4076 USD
---
## Findings
- **F1:** Down days of at least one usual daily move (z ≤ −1) are followed by a next-day excess return that grows as the close sits lower in the day's range: +0.75 % (t 2.74, 1217 cases on 484 days) for the lowest quarter, +0.26 % (t 0.69, 285 days) for closes in 0.25–0.5, and −0.19 % (t −0.24, 63 days) above mid-range. The low-close bounce holds well beyond the tested −2 threshold.
- **F2:** Moderate down days (z between −2 and −1, any close) are already followed by +0.56 % next-day excess (t 2.42, 1424 cases on 596 days). Flat days (|z| < 1) give −0.08 % (t −0.93, 2258 days), and up days of every size give between −0.54 % and +0.08 % with |t| < 1.2.
- **F3:** Among down days (z ≤ −1), the quartile whose prior 10-day return was strongest (10-day z above +0.14) bounces +0.98 % the next day (t 3.15, 459 cases on 254 days), the strongest cell in all my results. The two middle quartiles give −0.16 % (t −0.43) and +0.09 % (t 0.30), and the most fallen quartile gives +1.34 % (t 2.57, 207 days). The response is U-shaped, not graded.
- **F4:** Inside the tested capitulation days, the bounce is concentrated where the prior 5 days fell most. The deepest tercile (5-day return −15 % or worse) gives +3.01 % (t 1.91, 45 days) against +0.39 % (t 0.72) and +0.23 % (t 0.40) for the other two. Graded by the prior 10-day z instead, it is flat: +1.61 %, +0.90 %, +1.13 %.
- **F5:** The capitulation bounce lasts one day only. Days 2–3 after the case give −0.62 % excess (t −1.15, 127 days).
- **F6:** The capitulation bounce is concentrated in 2019–2022: 2020 gives +6.3 % (t 1.66, 10 days) and 2021 +2.2 % (t 1.77). 2023–2025 give −0.31 %, +0.38 % and −0.08 %, each with |t| < 0.8, and graded by volatility relative to its 60-day mean the terciles are −0.58 %, +0.87 % and +0.27 % (all |t| < 1).
- **F7:** The brief's reversal is absent; the opposite shows. After a 5-day run (|5-day z| > 1), flat-bodied days (|body| < 0.2 of range) in the widest-range tercile continue in the run's direction by +1.13 % the next day (t 2.13, 208 days), against −0.31 % and −0.44 % for the narrower terciles. This rests largely on 2020 (+4.6 %, t 2.28), and on the 3-day grid it is +1.62 % with t 1.45 (69 days).
- **F8:** After a strong 5-day rise, the top sextile of 5-day z (above +0.94) gives +0.33 % next-day excess (t 2.15, 992 days); the other five sextiles lie between −0.14 % and +0.04 %.
- **F9:** The book is carried by a few days. Its 10 best days hold 59 % of its summed daily gain, and its median day in the market is −0.04 % against a mean of +0.39 % (646 days with a non-zero return, max +21.7 %, min −12.0 %). This fits a Calmar of 0.72 despite a cost covered 7 times.

## Ideas
- `031-02.g1.b2.g1_low-close-down-day-bounce` (from F1, F2, F9): On a day a coin falls, the lower its close sits in that day's range, the more the coin rises over the next 1 day, and this holds already for falls of about one usual daily move, not only extreme ones.
- `031-02.g1.b2.g2_dip-in-uptrend-rebounds` (from F3, F2): On a day a coin falls, the stronger its 10-day return was before that day, the more the coin rises over the next 1 day.
- `031-02.g1.b2.g3_deeper-selloff-larger-bounce` (from F4, F5): On a day a coin falls far and closes near its low, the deeper its 5-day fall leading into that day, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
