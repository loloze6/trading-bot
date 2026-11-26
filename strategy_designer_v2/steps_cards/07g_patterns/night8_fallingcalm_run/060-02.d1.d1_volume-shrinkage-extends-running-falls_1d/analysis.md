---
line: 7.g patterns
backtest: 060-02.d1.d1_volume-shrinkage-extends-running-falls_1d
idea tested: 060-02.d1.d1_volume-shrinkage-extends-running-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6281 USD
---
## Findings
- **F1:** In a falling market (60-day return below -10 %), the bar of Saturday is followed by a mean next-day return of +0.97 % (t 4.88, 298 days), while the other weekdays' bars in the same market run from -0.58 % to +0.21 %, and Friday's bar is followed by -0.53 % (t -2.44). The Saturday rise is positive on all six coins (+0.56 % to +1.23 %; ETH, LTC, XMR and ZEC each with t above 2) and in 2018 (+1.76 %, t 6.60), 2019 (+0.96 %, t 2.39) and 2021 (+0.97 %, t 3.06). It is negative in 2020 (-1.37 %, t -2.21, 47 days). Outside falling markets the same bar has no consistent sign (2019 -0.39 %, 2020 -0.36 %).
- **F2:** The falling-market Saturday rise is graded by the fall before it. By 7-day return tercile it is +1.92 % (t 5.00) in the deepest third, +0.88 % (t 3.50) in the middle and +0.12 % (t 0.34) in the shallowest. By 60-day return tercile it is +1.92 % (t 5.29) in the deepest third against +0.54 % and +0.45 %. It barely depends on that day's volume against its 30-day mean (+0.92 %, +0.83 %, +1.17 %).
- **F3:** In running falls (60-day return below -10 % and 20-day return negative), the tested shrinkage effect sits in the deeper half of 20-day falls. There the 5-day unusual move is -4.35 % (t -2.78, 63 cases) in the lowest volume-ratio tercile, -2.52 % (t -2.44) in the middle and +0.57 % in the top. In the shallower half it is -1.64 % (t -0.87), -0.05 % and +1.85 %.
- **F4:** Inside the tested regime the edge is in the strongest signals only. The deepest-forecast quintile is followed by -4.13 % (t -3.58, 96 cases), and the two weakest quintiles by +1.45 % and +3.09 % (t 1.89), where the book is still short. Trades in the strongest entry-forecast quartile net +6.64 %, against +0.17 % in the weakest.
- **F5:** The shrinkage effect is not stable by year. In falling markets the lowest volume-ratio tercile is followed by -4.86 % in 2018 and -4.92 % in 2019, but +6.50 % in 2020 (15 cases) and +0.17 % in 2021. By coin it is carried by ETH (-7.09 %, t -2.53) and ZEC (-5.48 %, t -2.76).
- **F6:** The book gains on the coins' crash days. Its daily returns correlate -0.42 with the coins' mean. On its 20 largest days it averages +1.94 % while the coins average -5.86 %, with 15 of those 20 days positive.
- **F7:** The late-week rise in rising markets (Thursday or Friday bar, next day +1.18 %, t 4.76) is already held (045-01). A falling-market 5-day continuation after a down day relative to swing shows only in the second quintile (-3.43 %, t -3.06, against -1.67 % in the deepest), so it is not graded. It also reverses in 2020 (+6.87 %), so I do not use it.

## Ideas
- `060-02.d1.d1.g2_deep-fall-volume-dry-up-continuation` (from F3, F4): In a falling market, the more the coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, and the deeper its 20-day fall, the larger that effect.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.d1.d1.g1_falling-market-sunday-rebound` (from F1, F2): In a falling market, a coin rises over the day after Saturday's close, and the more it has fallen over its past 7 days, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
