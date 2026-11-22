---
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4065 USD
---
## Findings
- **F1:** Volume behind a fall works the opposite way to the brief. After a large one-day fall (the bottom fifth of the 1-day return measured in usual 4h moves), the third with the highest 1-day volume against its 30-day average rose +2.20 % more than the coin's normal 3-day drift (t 4.42, 334 non-overlapping cases), the middle third rose +0.58 % (t 1.15) and the lowest-volume third fell −0.21 % (t −0.50); Spearman rho between volume ratio and unusual move is 0.11 (p 0.0003, n 1001), while after large one-day rises the same volume split shows nothing (rho 0.03, p 0.27).
- **F2:** Large one-day falls are followed by a graded rebound with no streak and no 30-day regime needed. On the 6-bar grid, the decile with the deepest 1-day fall (below −3.99 usual moves) rose +0.62 % above drift over the next day (t 4.25, 1522 cases), the next decile rose +0.25 % (t 2.00), and the other deciles sat between −0.25 % and 0.00 %; Spearman rho is −0.098 (p < 0.0001, n 7473) among falls and −0.019 (p 0.10) among rises.
- **F3:** The same pattern shows inside down streaks of at least 3 bars. The unusual 3-day move rises with the 3-bar volume against the prior 30 bars, from −1.17 % (t −1.15) in the fading-volume quartile to +1.47 % (t 2.05) in the rising-volume quartile, 123–124 cases each.
- **F4:** On the 18-bar grid, the deepest decile of the current streak's loss in usual moves rebounded +1.02 % (t 2.42, 501 cases). With the 180-bar return above 0 the deepest fifth gave +1.53 % (t 3.37, 437 cases); with it below 0 the deepest fifth gave only +0.49 % (t 1.17, 420 cases). This is the tested idea's own effect, and it is concentrated in the deep tail.
- **F5:** 18-bar stretches starting on Sunday ended −1.23 % below drift (t −3.92, 811 cases). All 6 coins were negative (−0.92 % to −1.61 %) and 6 of 8 years were negative. It is a calendar effect with no graded situation.
- **F6:** The book's profit comes from long holds. Trades held over 520 hours made +24.4 % on average before fees (622 trades), while trades of 68–232 hours lost −1.04 % and −0.18 %. The book's year-by-year mean daily return tracks the coins' own (2018 −0.11 % vs −0.35 %; 2020 +0.40 % vs +0.42 %).
- **F7:** The top decile of the 6-day return in usual moves was followed by +0.99 % over 3 days (t 2.04, 501 cases), but this was carried by XRP (+3.07 %) and negative in 2018, 2019 and 2022. Given the number of angles examined, it does not stand out from chance.

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend.g1_capitulation-volume-fall-rebound` (from F1, F3): After a large one-day fall measured in the coin's usual 4-hour moves over the past 30 days, the higher the volume of that day against the coin's 30-day average volume, the larger the coin's rise over the next three days.
- `024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend.g2_one-day-fall-graded-rebound` (from F2, F4): The larger a coin's 1-day fall measured in its usual 4-hour moves over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
