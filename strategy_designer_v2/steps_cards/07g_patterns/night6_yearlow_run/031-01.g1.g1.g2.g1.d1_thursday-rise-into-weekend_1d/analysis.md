---
line: 7.g patterns
backtest: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
idea tested: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4031 USD
---
## Findings
- **F1:** Across all weekdays, a coin's 14-day fall is followed by a reversal. On the non-overlapping 2-day grid, among bars whose 14-day return is at or below 0, the excess 2-day return falls as the 14-day return rises: slope −0.49 % per standard deviation of the 14-day return, t −4.57, 3831 cases. A deeper fall is followed by a larger gain.
- **F2:** This reversal after 14-day falls is broad. The slope is negative on all 6 coins (t from −1.49 on ZEC to −2.89 on XRP). It is negative in 7 of 8 years, with t below −2 in 2019, 2021, 2022, 2024 and 2025; only 2020 is positive (t +0.99). It persists over 4 days on the 4-day grid (slope −0.78 %, t −3.49, 1850 cases).
- **F3:** The reversal after 14-day falls is not the tested weekend effect, and it is stronger once Thursday and Friday bars are removed (slope −0.91 %, t −6.73, 2737 cases). On Friday bars the sign flips (slope +0.58 %, t +3.70, 1097 cases). By quintile it is carried mostly by the deepest-fall quintile, whose excess 2-day return is +0.63 % (t 1.99, 777 cases), while the other four quintiles are at or below 0.
- **F4:** One-day drops also reverse. On the 2-day grid, among down days, a larger drop is followed by a larger excess 2-day return (slope −0.43 % per standard deviation, t −3.91, 4185 cases), and the lowest one-day-return quintile is followed by +0.52 % (t 2.64). Within this, the slope is concentrated in the highest 20-day-volatility tercile (−0.89 %, t −3.58), against t −1.46 and −0.88 in the lower two terciles.
- **F5:** The rising-coin gradient the book trades exists only on Thursday bars. On Thursday bars, the slope of the excess 2-day return on the positive 14-day return is +1.31 % (t 6.77, 1094 cases). Pooled over all weekdays on the 2-day grid it is nil (slope +0.07 %, t 0.64, 3811 cases). By year it swings from −0.98 % (t −1.87) in 2019 to +1.82 % (t 3.22) in 2024.
- **F6:** The book earns all of its gain on two weekdays, the bars starting Thursday (+0.176 %, t 4.19) and Friday (+0.230 %, t 5.18). It loses its fees on the Wednesday bar (−0.027 %, t −7.56) and is near 0 on the other days.
- **F7:** The plain weekend drift behind the book is narrow. The Friday and Saturday 1-day excess returns are +0.25 % (t 2.63) and +0.30 % (t 3.76), but by coin only XMR is clearly positive (+0.40 %, t 3.02), and by year only 2021 reaches t above 2 (+0.56 %, t 2.45).

## Ideas
- `031-01.g1.g1.g2.g1.d1.g1_two-week-fall-rebound` (from F1, F2, F3): After a 14-day fall, a coin's 14-day return grades its gain over the next 2 to 4 days: the deeper its two-week fall, the larger its rebound over those days.
- `031-01.g1.g1.g2.g1.d1.g2_volatile-one-day-drop-rebound` (from F4): When a coin's 20-day volatility is high, its one-day return grades its gain over the next 2 days: the larger the day's drop, the larger the rebound over the following 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
