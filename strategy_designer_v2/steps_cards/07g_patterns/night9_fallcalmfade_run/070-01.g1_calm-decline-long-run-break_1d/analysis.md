---
line: 7.g patterns
backtest: 070-01.g1_calm-decline-long-run-break_1d
idea tested: 070-01.g1_calm-decline-long-run-break
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4397 USD
---
## Findings
- **F1:** In falling calm bars, the next-day fade after a break grows with run length, but only at the long end and not steadily. Breaks of runs of 4 or more down days were followed by an excess move of −1.80 % (t −3.04, 58 cases on 44 days). Breaks of a single down day gave −0.24 % (t −0.57, 226 cases on 133 days). Runs of 2 gave −0.91 % (t −1.48) and runs of 3 gave −0.26 % (t −0.46).
- **F2:** The fade keeps growing past the one-day horizon the book holds.
- **F3:** In falling calm, the fade is graded more cleanly by how deep the run fell than by how many days it lasted. Depth here is the run's fall divided by the coin's 20-day daily swing, cut into thirds.
- **F4:** In falling calm, the fade belongs to up days that break a down run, not to up days in general. Up days that broke no run and closed near their high were followed by +0.73 % (t 1.14, 130 cases). Breaks closing near their high were followed by −1.01 % (t −2.66, 160 cases on 106 days).
- **F5:** The effect and the book's gain sit mostly in 2018.
- **F6:** Outside falling calm, run breaks also fade in falling (agitated) bars but not in rising ones.
- **F7:** Among the many angles examined, falling calm days showed a weekday pattern: after Saturdays +0.57 % (t 3.12, 269 cases), after Mondays −0.84 % (t −2.67, 265 cases). It is not graded and stands out only modestly given how many groupings were looked at, so no idea is drawn from it.

## Ideas
- `070-01.g1.g1_calm-decline-deep-run-fade` (from F3, F1, F4): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next day. The fall is larger the deeper the run's fall was, measured as the run's total return against the coin's typical daily swing over the past 20 days.
- `070-01.g1.g2_calm-decline-run-break-three-day-fade` (from F2, F1): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next three days. The fall is larger the more down days that run held beyond the first.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
