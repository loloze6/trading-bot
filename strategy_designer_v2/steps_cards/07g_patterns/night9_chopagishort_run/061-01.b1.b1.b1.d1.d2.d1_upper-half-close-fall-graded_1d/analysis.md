---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6348 USD
---
## Findings
- **F1:** The book's gain comes from one window. Its daily returns sum to +0.236 over folds B and C, but only +0.00045 once w16 is removed. Its 5 best days sum to +0.355, more than the whole book. The 12 trades in w16 average +22.1 % net, while the 139 trades overall win only 36 % of the time. So the confirmed size (+2.24 % unusual move per case, 10 times the 0.22 % trade cost) is not spread across windows.
- **F2:** Inside the choppy agitated profile the situation is rare and its fall is not clear. The profile covers 4.4 % of the 5-day grid cells. Closes in the top quarter after a negative 5-day return show −3.06 % over 2 days (t −1.83, 28 cases, 25 days) and −8.49 % over 5 days (t −1.51, only 9 cases).
- **F3:** Outside the profile the same situation does fall, but over 1 to 2 days rather than 5. After a negative 5-day return, a close at 0.75–0.9 of the day's range is followed by −1.06 % the next day (t −2.77, 558 cases, 290 days) and −1.76 % over 2 days (t −2.45, 267 cases, 142 days). Over 5 days the top-quarter groups show nothing (t −0.84).
- **F4:** That 2-day fall is graded by the depth of the 5-day fall. Among top-quarter closes after a negative 5-day return outside the profile, the deepest tercile falls −3.45 % (t −2.87, 132 cases, 60 days), the middle tercile −0.99 % (t −1.19) and the shallowest −0.09 % (t −0.17).
- **F5:** The grading holds across all profiles when the fall is scaled by the coin's own swing. Over 2 days, for upper-half closes after a negative 5-day return, the strength regressed on the 5-day return divided by the 30-day swing has slope +0.135 in calm markets (t 3.92, n 420) and +0.086 in agitated markets (t 1.72, n 448). In both, the deepest tercile has a strength of about −0.30 (−2.3 % over 2 days).
- **F6:** The effect needs both the high close and the prior fall:
- **F7:** The fade is larger when the coin swings more. Among top-quarter closes after a negative 5-day return outside the profile, the 2-day move is −3.54 % in the highest swing tercile (t −2.29) against −0.24 % in the lowest (t −0.35). It holds in three of four years: 2018 −3.42 % (t −2.39), 2019 −1.23 % (t −2.33), 2021 −1.77 % (t −1.29), against 2020 +0.18 %.

## Ideas
- `061-01.b1.b1.b1.d1.d2.d1.g2_choppy-agitated-two-day-fade` (from F1, F2, F3, F4): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range after its 5-day return has been negative, its price falls over the next two days. The deeper the 5-day fall, the larger the fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d2.d1.g1_strong-close-in-slide-fades` (from F3, F4, F5, F6, F7): In any market, when a coin's daily close sits near the top of that day's high-low range after a 5-day fall, its price falls over the next two days. The deeper the 5-day fall, measured against the coin's own daily swing over the last 30 days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
