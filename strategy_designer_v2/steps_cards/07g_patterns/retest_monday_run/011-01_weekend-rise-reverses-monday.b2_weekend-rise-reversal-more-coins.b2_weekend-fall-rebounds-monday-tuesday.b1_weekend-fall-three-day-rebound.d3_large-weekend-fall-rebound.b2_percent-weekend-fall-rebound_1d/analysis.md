---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5233 USD
---
## Findings
- **F1:** Thin volume, not depth alone, carries the Sunday-fall rebound. Among Sunday falls, the slope of the drift-adjusted 3-day return on Sunday's return is -0.917 (t -5.02, n 616) in the lowest tercile of Sunday volume relative to its 30-day mean, -0.216 (t -1.30) in the middle tercile and +0.073 (t +0.64) in the highest. In a regression on depth, thinness and their product, depth alone is 0.066 (t 0.82) and depth × thinness is 0.386 (t 3.38), over 1830 cases.
- **F2:** This volume grading belongs to the weekend. Tuesday-to-Thursday falls show no such ordering: their slope is -0.141 (t -1.67) in the low-volume tercile and -0.153 (t -3.29) in the high-volume tercile, over about 1966 cases each.
- **F3:** Sunday rises also reverse, unlike rises on Monday to Wednesday. The 3-day drift-adjusted return after a Sunday rise is -1.01 % (t -5.57, n 2480), against -0.48 %, 0.00 % and +0.35 % after rises on Monday, Tuesday and Wednesday. The reversal is not graded by the rise's size (quartile means -1.17 %, -0.70 %, -0.92 %, -1.15 %). It is largest on thin Sunday volume (-1.57 %, t -5.44, n 643, against -0.62 % and -0.82 % in the other terciles). A short earns a total move of +0.56 % (t 2.94, n 1929), 2.6 times the 0.22 % cost of a trade.
- **F4:** Across all Sundays, both signs together, the reversal slope of the 3-day drift-adjusted return on Sunday's return falls steadily as Sunday's relative volume rises: -0.688 (t -7.92), -0.282 (t -3.95) and -0.120 (t -2.82), over about 1260 cases per tercile.
- **F5:** The rebound after a Sunday fall comes almost entirely from high-volatility periods. By tercile of the coin's 20-day volatility, the mean drift-adjusted 3-day return is -0.01 %, +0.11 % and +2.76 % (n 690 each), with depth slopes t -0.61, -1.81 and -2.63.
- **F6:** The book's profit and risk sit entirely on Monday to Wednesday. Its mean daily return is +0.121 %, +0.005 % and +0.100 % on those days, with daily standard deviations of 1.2-1.3 %. All 115 of its best-2 % and worst-2 % days fall on Monday to Wednesday, none on Thursday to Sunday. The edge is unstable by year: the Sunday-fall mean is -2.89 % in 2018 and -1.08 % in 2022, against +2.42 % in 2021 and +2.18 % in 2024, which fits the 0.30 Calmar.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound.g1_thin-volume-sunday-fall-rebound` (from F1, F2, F4): A coin's Sunday close-to-close fall is followed by a rise over the next 3 days. That rise is larger the deeper the fall and the lower Sunday's volume is against the coin's own 30-day average volume.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound.g2_thin-sunday-rise-fades` (from F3, F4): A coin's Sunday close-to-close rise is followed by a fall over the next 3 days. That fall is larger the lower Sunday's volume is against the coin's own 30-day average volume.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound.g3_volatile-regime-weekend-fall-rebound` (from F5, F6): A coin's Sunday close-to-close fall is followed by a rise over the next 3 days. That rise is larger the higher the coin's volatility of daily returns over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
