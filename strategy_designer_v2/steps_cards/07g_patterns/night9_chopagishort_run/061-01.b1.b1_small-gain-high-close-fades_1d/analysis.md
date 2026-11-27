---
line: 7.g patterns
backtest: 061-01.b1.b1_small-gain-high-close-fades_1d
idea tested: 061-01.b1.b1_small-gain-high-close-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4422 USD
---
## Findings
- **F1:** Inside the choppy, agitated profile, the coin's 5-day unusual move falls steadily as the close moves up the day's range. Closes in the top fifth move -3.02 % (t -2.50, 75 cases on 63 days), the 0.6–0.8 band -1.94 % (t -1.28, 80 cases) and the middle band -1.04 % (t -0.48, 78 cases). The Spearman correlation between close location and the 5-day unusual move over the 191 in-profile cases is -0.18.
- **F2:** The fade lives only inside the profile. Outside it, closes in the top fifth move +0.11 % over 5 days (t 0.21, 1,314 cases on 503 days), and no close-location band outside reaches |t| 0.5. Across all bars of folds B and C without the profile, top-fifth closes move +0.35 % (t 0.30, 410 cases).
- **F3:** Among in-profile closes in the top fifth, the fall comes from days that did not gain much. The tercile gaining under 0.57 usual daily moves falls -5.94 % (t -2.71, 23 cases) and the 0.57–1.27 tercile falls -3.92 % (t -2.33, 23 cases), while the strongest-gain tercile moves +0.03 % (t 0.01). The step-5 median split, made only among cases already below one usual move, found no further gradient inside small gains (-0.47 %).
- **F4:** Over 2 days instead of 5, in-profile high closes move only -1.07 % (t -0.67, 40 cases) and the 0.6–0.8 band -1.41 % (t -1.49). The move needs about the five days the tested idea used, not the brief's two.
- **F5:** Everything else I looked at stood out from chance nowhere, given about twenty angles checked. These covered close location, scaled 1-day and 3-day returns, range size, the volatility ratio, the 60-day trend, weekday and year, across all bars. None reached |t| 2 except a 16-case low-close bucket in a flat 60-day trend (-5.2 %, t -2.44), too thin to count.
- **F6:** The book is a pure short on rare bars. It is in a position on about 4.5 % of bars, and its active-day returns correlate -0.82 with the coin's. Its 63 trades average +1.50 % net, with 48 % winners, a median hold of 5 days and spread across coins: XMR -2.69 % over 12 trades, ZEC +2.27 % over 16. So its gain is a few large falls, not a steady edge.

## Ideas
- `061-01.b1.b1.g1_choppy-agitated-close-height-fade` (from F1, F2, F4): In a choppy, agitated market, the nearer a coin's daily close sits to the top of that day's high-low range, the more its price falls over the next five days.
- `061-01.b1.b1.g2_high-close-without-gain-fades` (from F1, F3, F4): In a choppy, agitated market, a coin whose daily close sits near its high falls over the next five days, and the higher that close sits in the range relative to the day's gain (measured in the coin's usual daily moves), the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
