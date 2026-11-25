---
line: 7.g patterns
backtest: 032-02.g1.b1_uptrend-near-high-more-coins_1d
idea tested: 032-02.g1.b1_uptrend-near-high-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6817 USD
---
## Findings
- **F1:** Among bars where the coin had risen over 28 days (5-day grid, 941 cases), the raw ratio of the close to its 28-day highest close separates the next 5 days strongly: the top fifth (within 0.7 % of the high) had an excess return of +5.43 % (t 2.33, 188 cases), the bottom fifth (12.7 % to 46 % below the high) had −3.11 % (t −3.48, 188 cases), and top minus bottom was +8.53 % (Welch t 3.42). The middle fifths do not rise in order (+1.83 %, −0.31 %, +0.99 %), and this t is not grouped by day.
- **F2:** That raw-proximity relation in rising coins has a positive Spearman correlation in 9 of 12 windows (pooled 0.121, 941 cases; w18 0.430, w16 0.274, w12 0.257). The tested forecast, which standardises proximity against its own past 60 values, reached only Welch t 0.94, so the plain distance from the high carries the effect the test diluted.
- **F3:** Among coins that had risen over 28 days, the size of the 14-day rise orders the next 5 days' excess return in every step: −1.88 %, +0.44 %, +1.13 %, +1.96 %, +3.18 % from the lowest to the highest fifth (top minus bottom +5.06 %, Welch t 1.98, 188 cases per fifth). This is not beyond chance given the number of angles examined.
- **F4:** The brief's calm-decline claim shows only weakly. Among falling coins with below-usual 20-day volume, a deeper 28-day fall goes with a lower excess 5-day return (slope on rank −0.0586, t −1.75 with the cases of one day grouped, 502 cases on 130 days; Spearman negative in 8 of 11 windows). Among falling coins with a below-usual daily range, deeper falls did not keep falling: the deepest fifth was −1.04 % and top minus bottom +1.90 % (t 1.11).
- **F5:** Among falling coins with wider-than-usual daily ranges, the deepest 28-day falls (40 % to 61 %) were followed by +4.39 % excess over 5 days, against −2.85 % for the shallowest fifth (top minus bottom −7.24 %, Welch t −2.35). Grouped by day it is weak (slope t 1.43, 250 cases on 58 days), so a rebound after violent falls is only suggested.
- **F6:** Among falling coins, those 22 % to 28 % below their 28-day high close (second fifth) and 17 % to 22 % below (third fifth) had excess 5-day returns of −4.05 % (t −4.24) and −3.37 % (t −4.29). The correlation over the whole range is not graded, though (pooled Spearman 0.074, and of mixed sign across the 12 windows).
- **F7:** The book behaves mostly like the coins themselves. Its worst tenth of days (−4.55 % mean) came on coin days averaging −7.09 %, after a mean prior 28-day rise of +28 %. Its best tenth (+6.29 %) came on coin days averaging +9.45 %, after prior 5-day and 28-day rises of +20 % and +45 %.
- **F8:** Next-day excess returns by weekday were −0.36 % on Mondays (t −2.59) and +0.39 % on Fridays (t 2.94), about 1,750 coin-days each. These are not grouped by day, and with 7 groups this is a pattern by calendar, not a graded one.

## Ideas
- `032-02.g1.b1.g1_uptrend-pullback-keeps-sagging` (from F1, F2, F6): Among coins that have risen over the past 28 days, the further the day's close has pulled back below the highest close of those 28 days, the more the coin falls short of its usual rise over the next 5 days, down to an outright fall for the deepest pullbacks.
- `032-02.g1.b1.g2_two-week-momentum-inside-uptrends` (from F3, F7): Among coins that have risen over the past 28 days, the larger their rise over the past 14 days, the larger their rise over the next 5 days beyond their usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
