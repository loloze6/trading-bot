---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4388 USD
---
## Findings
- **F1:** Inside the choppy agitated profile, on the 5-day grid of folds B and C, closes in the top fifth of the day's range were followed by a 5-day move 7.18 % below the coin's drift (t −2.80, 21 cases on 16 days). Closes in the 0.6–0.8 band were followed by −4.57 % (t −0.96), and closes in the bottom fifth by −1.22 % (t −0.49).
- **F2:** The fall inside the profile is graded by where the close sits in the day's range, not by the day's width. By close location tercile the unusual 5-day move was −0.11 %, −3.62 % and −5.96 % (top tercile t −2.09, 29 cases, 20 days), with a Spearman correlation of −0.215 between close location and the move. By range-multiple quartile it was −5.11 %, −0.51 %, −9.29 % and +1.86 %, with the widest days showing no fall (t +0.51, 10 cases).
- **F3:** Among closes in the top fifth of the range inside the profile, the fall appears whatever the 5-day return. After a negative 5-day return it was −10.5 % (t −2.14, 8 cases); after a positive one it was −5.2 % (t −2.09, 13 cases).
- **F4:** The pattern needs the agitation. In choppy markets outside the agitated profile, closes in the top third of the range were followed by +4.26 % against drift (t +1.54, 52 cases, 32 days), against −9.88 % in choppy agitated (t −2.01, 8 cases). Outside the profile no close-location bin shows a fall: all bins from 0.4 upward lie between +0.76 % and +1.06 %, with |t| ≤ 1.06.
- **F5:** Inside the profile the fall grows as the coin's 10-day swing rises against its 30-day swing: −2.91 %, −6.32 % and −11.65 % by tercile, with the top tercile at t −2.01 on 18 cases and 12 days. This is one angle among about a dozen I looked at, so it is suggestive, not decisive.
- **F6:** The effect is thin in time and not uniform. The profile covers 131 of 9,986 bars in the mean-reversion regime. By year inside the profile the unusual move was −14.6 % (2018, 5 cases), −3.7 % (2019, t −2.68), −6.0 % (2020) and +1.0 % (2021, t +0.40). Weekday showed nothing (all |t| < 1.25).

## Ideas
- `061-01.b1.b1.b1.d1.d1.d3.d2.g1_close-near-high-five-day-fade` (from F1, F2, F3, F4): In a choppy, agitated market, the nearer a coin's daily close sits to the top of that day's high-low range, the more its price falls over the next five days, whatever its 5-day return before.
- `061-01.b1.b1.b1.d1.d1.d3.d2.g2_widening-swing-upper-close-fade` (from F5, F1, F4): In a choppy, agitated market, a coin whose daily close sits near the top of that day's range falls more over the next five days the higher its swing over the last 10 days stands against its swing over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
