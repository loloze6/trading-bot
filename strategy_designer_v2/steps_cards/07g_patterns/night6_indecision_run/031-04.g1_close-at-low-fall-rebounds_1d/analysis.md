---
line: 7.g patterns
backtest: 031-04.g1_close-at-low-fall-rebounds_1d
idea tested: 031-04.g1_close-at-low-fall-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4135 USD
---
## Findings
- **F1:** Holding the book did not beat holding the coins, and its gain rests on a few days. On its 406 active days the book's mean daily return was +0.086 %, but its 10 best days add +46.6 % and make up 133 % of its total gain, against −34.9 % for its 10 worst days.
- **F2:** The tested idea's own situation is not carried by the sharpest falls. Next-day excess return after days with z ≤ −3 was +0.87 % (t 0.53, 86 cases, 37 days), and after −3 < z ≤ −2 it was +0.50 % (t 1.19, 325 cases, 162 days).
- **F3:** Milder down days rebounded more reliably than sharp ones, but not in a graded way. Days with −2 < z ≤ −1 were followed by +0.56 % next-day excess (t 2.42, 1424 cases, 596 days). Yet across all days with z ≤ −1, the slope of next-day excess on the size of the fall was flat (t 0.14, 1835 cases, 631 days). The rebound does not grow with the fall.
- **F4:** Within sharp down days, the close-at-low effect appeared only as a step, not a grade. Closes 80–95 % of the way to the low gave +1.46 % (t 1.93, 183 cases), and closes at the very low gave +1.05 % (t 1.53, 53 cases). Closes at 50–80 % gave −0.26 % (t −0.32, 151 cases).
- **F5:** The brief's own pattern points the other way: wide flat days inside runs were followed by continuation, not reversal. The reversal was −0.98 % (t −2.63, 626 cases, 433 days) in the widest-range quartile. This does not hold up in two ways:
- **F6:** Sharp down days rebounded strongly only in each coin's highest-volatility quartile, +4.09 % (t 2.18, 71 cases, 39 days). This is a coin-level split and does not survive the relative version. Measured against the coin's own 120-day median volatility, the top quartile gave −0.84 % (t −0.49, 42 cases). The slope on that relative volatility had a t of 1.14 (166 cases, 70 days).
- **F7:** The other angles showed nothing that stands out:

## Ideas
- No ideas: Across roughly thirty angles, no pattern beyond the tested idea stood out enough. The tested angles were the forecast's close location, the size of the fall, the 3- and 5-day horizons, wide flat days in runs, volatility level absolute and relative, weekday, the prior run and year. No result reached a t near 3, and the few near 2 were either not graded (F3, F4), changed sign across years (F5), or vanished under a relative measure (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
