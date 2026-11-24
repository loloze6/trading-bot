---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d
idea tested: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4280 USD
---
## Findings
- **F1:** On days after a 5-day fall whose range was over 1.4 times the 20-day mean range and which closed in the top fifth of that range, the coin's unusual 3-day move was −3.90 % (t −2.21; 114 cases on 45 days; rises in only 33 % of cases), while the same wide down-run days closing in the middle of the range (location 0.4–0.8) were followed by +2.9 % and +3.2 % (t 1.77 and 1.73).
- **F2:** Within those wide down-run days closing near their high, the move grew with the day's width: −1.85 % for 1.4–2 times the mean range (t −1.40; 77 cases, 42 days), −7.93 % for 2–3 times (t −3.09; 32 cases, 8 days) and −9.56 % above 3 times (t −4.52; 5 cases, 3 days), with rises in 42 %, 19 % and 0 % of cases.
- **F3:** The same pattern was negative in 5 of the 7 years with enough cases (2025: −8.6 %, t −2.95, 26 cases on 6 days; 2022: −5.5 %, t −1.43). It falls on few days, so much of it may come from market-wide selloffs rather than from each coin alone.
- **F4:** Across wide down-run days in general, where the close landed in the range barely ranked against the following move (Spearman rho −0.03, n 1729). The effect sits only in the top close location and does not run through the whole range.
- **F5:** The tested situation (flat, wide day after a 5-day rise) was positive in 5 of 7 years but clearly negative in 2024 (−3.8 %, t −2.60; 21 cases, 18 days). The book's 20 best days carried 69 % of its total gain.
- **F6:** The book's trades that lasted 3.5–6 days earned +10.8 % net on average (38 trades) against +1.6 % for those of about 3 days (435 trades). These longer trades are ones extended by fresh signals, so this is selection rather than a pattern in the bars.
- **F7:** Many other angles showed nothing that stands out from chance: the next 3 days after each fifth of the 1-day return (|t| ≤ 0.84), after each fifth of the 5-day return by volatility tercile (|t| ≤ 2.2 over 15 cells), by weekday (|t| ≤ 1.31), and wide up-run days by flatness or close location (|t| ≤ 1.62).

## Ideas
- `031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation` (from F1, F2, F3, F4): After a coin has fallen over the past 5 days, a day whose range is wide against its average daily range over the past 20 days and which closes near its high is followed by a further fall over the next 3 days; the wider that day's range, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
