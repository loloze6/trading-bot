---
line: 7.g patterns
backtest: 060-01.b1_falling-agitated-high-close-fade-wider_1d
idea tested: 060-01.b1_falling-agitated-high-close-fade-wider
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3805 USD
---
## Findings
- **F1:** Inside the falling-agitated profile, the next day after a close in the top fifth of the range rose +0.20 % (t 0.23, n 59), and after a close in the 0.6–0.8 band it fell −0.80 % (t −1.43, n 82), so the fall does not grow toward the high; the only clear location effect runs the other way, with closes in the bottom fifth followed by +1.65 % (t 2.62, n 82).
- **F2:** The book earns nothing on the explore half: its active-day gain was +0.11 % on ZEC (t 0.55, n 120), −0.15 % on BCH (t −0.41) and −0.19 % on DOGE (t −0.46), with no year above t 1.6 (2018 +0.71 %, 2020 −0.25 %).
- **F3:** On all bars, a day whose close-to-close move is very small against the coin's 20-day swing (bottom fifth of |return|/swing) was followed by a next-day return of −0.67 % (t −2.50, n 444). The quintile means rise steadily to +1.03 % (t 3.06) for the largest moves, a correlation of next return with |return|/swing of +0.07.
- **F4:** The quiet-day fall shows both inside the profile (−1.44 %, t −2.30, n 74) and outside it (−0.52 %, t −1.74, n 370), and on every coin (BCH −0.19 %, DOGE −1.19 %, ZEC −0.29 %). It is not steady over time: 2018 −1.19 % (t −2.13) and 2021 −0.79 % (t −2.37), but 2020 +0.34 % (t 1.02). It is gone over three days (−0.25 %, t −0.46, n 305 on the 3-day grid). Given the ~25 groupings looked at, this is a weak pattern, not a strong one.
- **F5:** Large down days (bottom fifth of return/swing) were followed by +1.19 % (t 3.76, n 444), and +1.76 % inside the profile (t 2.50, n 82). Heavy-volume days (top fifth of volume against its 20-day median) were followed by +0.80 % (t 2.37). This is the rebound after a sharp fall that the map already holds in falling agitated (16 long strategies), so it is not a discovery.

## Ideas
- `060-01.b1.g1_quiet-day-next-fade` (from F3, F4): After a day whose close-to-close move is unusually small for the coin, measured as its one-day return against the standard deviation of its daily returns over the past 20 days, the coin falls over the next day; the smaller that move against its recent swing, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
