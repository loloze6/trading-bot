---
line: 7.g patterns
backtest: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d
idea tested: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4121 USD
---
## Findings
- **F1:** The rebound sits in the volatile regime and its deepest tail: there, next-day excess return falls as the day's return in usual moves rises (r −0.23, t −8.6, 1407 down days), against r 0.004 (t 0.29, 5873 days) outside it. Volatile-regime falls of 2.5 usual moves or more average +6.88 % next day (t 4.56, 51 cases), while falls of 1.5 to 2.5 moves average only +0.92 % (t 1.22, 104).
- **F2:** Among falls of at least 1.5 usual moves in the volatile regime, the next-day excess return grows with the day's volume against its 20-day average: +0.51 % (t 0.53, 50) in the low third, +2.02 % (t 2.19, 39) in the middle third, +5.18 % (t 3.59, 66) in the high third. Outside the regime the same falls show no volume grading (−0.17 %, +0.35 %, −0.11 %, every t under 1.3).
- **F3:** In the volatile regime, the next-day excess return falls steadily with where the day closes in its high-low range, across all days: +1.09 % (t 4.46, 651) in the quintile closing nearest the low, then +0.22 %, −0.08 %, −0.37 %, −0.38 %. Among big falls in that regime, closes in the bottom third of the range average +3.50 % (t 4.25, 123), against +0.47 % (t 0.29, 32) in the middle third. Outside the regime the spread is small (+0.15 % with t 1.69 to −0.19 % with t −2.28). This test does not separate the close's place in the range from the fall's size.
- **F4:** The big-fall rebound is concentrated in time. Falls of at least 1.5 usual moves earn +1.83 % (t 2.21) in 2020 and +2.31 % (t 3.36) in 2021, but between −0.50 % and +0.11 % (every t under 0.9) in each year from 2022 to 2025. Among coins only XMR stands out (+1.14 %, t 2.62); BTC earns +0.01 % (t 0.04).
- **F5:** The book's gain rests on rare days: its daily return is +10.9 % at the 99.9th percentile and +2.07 % at the 99th, against a median of 0. Trades in the top entry-forecast quarter net +0.69 % on average, while the two middle quarters lose 0.61 % and 0.30 %.
- **F6:** Up days in the volatile regime tend to be followed by a fall, but not in a graded way and not strongly: up days of 0 to 0.75 usual moves average −0.35 % next day (t −1.92, 943), and those of 0.75 to 1.5 moves −0.83 % (t −2.54, 305). Up days of 1.5 to 2.5 moves break the grading at +0.07 % (t 0.13, 123). Given the many angles examined, this does not stand out from chance.

## Ideas
- `031-01.g1.g1.g1.g3.g1_volume-heavy-drop-next-day-rebound` (from F2, F1): When a coin's last 20 days have been unusually volatile for it, the heavier a down day's volume against its average over the past 20 days, the more the coin rises over the next day.
- `031-01.g1.g1.g1.g3.g2_close-at-low-volatile-rebound` (from F3, F1): When a coin's last 20 days have been unusually volatile for it, the closer a day's close sits to that day's low within its high-low range, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
