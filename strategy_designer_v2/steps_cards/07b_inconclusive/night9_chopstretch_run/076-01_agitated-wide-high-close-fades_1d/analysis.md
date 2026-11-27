---
line: 7.b inconclusive
backtest: 076-01_agitated-wide-high-close-fades_1d
idea tested: 076-01_agitated-wide-high-close-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3447 USD
---
## Findings
- **F1:** In folds B and C, the test's cases (forecast < 0, 692 cases) fall more than the drift the next day, as the idea predicts (short-direction unusual move +0.56 %, t 1.47). This sits on the same side as step 5's full-data result (+0.29 %, t 1.29, 827 days), but short of the t of 2.
- **F2:** The effect is not tied to a few windows. It is positive in 9 of the 11 windows with more than one case, with no single window above a t of 2.2 (w9 +1.59 %, t 2.17). It is negative only in w11 (−0.36 %, t −0.37, the window with the most cases, 151) and w12 (−1.19 %, t −0.92). Its weakness is a small mean against a 4.7 % daily move, so these case counts cannot show it clearly.
- **F3:** The effect is positive on all six coins and strongest on XMR (+1.64 %, t 2.71, 84 cases) and ETH (+0.94 %, t 1.38). It is near zero on BTC (+0.10 %, t 0.26) and LTC (+0.05 %, t 0.08), so each coin adds little evidence alone and more coins would add cases.
- **F4:** The effect shows at the plan's one-day horizon and fades after it: +0.56 % at 1 day, against +0.22 % (t 0.46) at 2 days, +0.39 % (t 0.60) at 3 days and +0.51 % (t 0.73) at 5 days. The plan measured the idea where it shows.
- **F5:** The effect is mixed by trend. Cases in a falling 60-day trend fall +1.93 % (t 2.21, 90 cases), choppy ones +3.03 % (t 1.62, 24 cases), and rising ones −0.10 % (t −0.12, 160 cases). The brief's claim that it holds in any trend, rising included, is not seen in these folds.
- **F6:** The grading is weak in folds B and C. The strongest and weakest forecast quartiles both give +1.09 % (t 2.14 and 1.38). The highest-close quartile gives +0.18 % (t 0.32), against +1.13 % for the second. Agitated narrow high-close days give +0.40 % (t 1.33, 1109 bars), close to wide ones at +0.67 % (t 1.50, 527 bars). Even so, step 5's supporting check on all folds passed (+0.28 %).
- **F7:** The same wide high-close days in calm markets do not fall (−0.02 %, t −0.07, 846 bars), against +0.67 % in agitated markets. This is the contrast the brief predicts.

## Ideas
- `076-01.b1_agitated-wide-close-fade-more-coins` (from F1, F2, F3, F4, F7): In an agitated market, a day whose high-low range is wide against the coin's average range over the past 20 days and which closes near its high is followed by a fall over the next day. The fall is larger the wider the day's range and the closer its close sits to its high, the two multiplying, so a high close on an ordinary-width day is followed by little fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
