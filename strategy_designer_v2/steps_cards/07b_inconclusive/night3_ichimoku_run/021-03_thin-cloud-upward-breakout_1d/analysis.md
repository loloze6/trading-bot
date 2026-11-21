---
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout_1d
idea tested: 021-03_thin-cloud-upward-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3409 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but rests on a few large winners. Across 152 upward cloud crosses the mean unusual 26-day return is +4.87 % (t 1.55). Yet the median case is −1.8 % and only 44 % of cases are positive. The returns are strongly skewed (skew 4.47, sd 38.8 %). Dropping the top 5 % of cases turns the mean to −1.3 % (t −0.78).
- **F2:** The effect is mostly the market's own year. 2020 gives +26.1 % (t 3.40, 19 cases, 74 % positive) and 2021 gives +20.5 % (t 1.55, 18 cases). 2018 gives −19.8 % (t −2.89, 11 cases, 9 % positive), 2022 −6.6 % (t −1.48) and 2025 −5.6 % (t −1.29). The other years are near zero, so whether a cross is followed by a rise depends on the bull or bear year it falls in.
- **F3:** The thinness grading, the brief's own claim, is absent. The thin-minus-thick difference is +0.23 %. The rank correlation of cloud proximity with the unusual 26-day return is −0.02 (raw) and +0.02 (standardised). The raw-proximity quartiles run +0.9 %, +6.5 %, +12.4 %, −0.3 % with no order. More data would not make this grading appear.
- **F4:** Every coin is positive but none is clear. BTC is +0.4 % (t 0.13, 21 cases), ETH +0.2 % (t 0.04), LTC +4.5 % (t 1.16), XMR +3.0 % (t 0.68), XRP +12.6 % (t 0.98, median −12.1 %) and ZEC +5.1 % (t 0.77). The sign is consistent but too small for 21 to 32 cases per coin to show.
- **F5:** The horizon is not the problem. The unusual return is +0.9 % at 5 days (t 1.01), +2.4 % at 10 days (t 1.62) and +4.9 % at 26 days (t 1.55). At 52 days it vanishes (−0.5 %, t −0.08, 112 cases), so the move is built within the plan's 26 days and fades afterwards.
- **F6:** The rise after a cross is larger the more the coin had fallen over the 26 days before it. By quartile of the past 26-day return, the mean unusual 26-day return runs +12.6 % (t 1.38, 59 % positive), +10.1 %, +5.6 % and −4.2 % (t −1.00, 33 % positive), with 27 cases each. The 52-day past return shows no such order.
- **F7:** Cost does not explain the failing book. The total move per case (+9.44 %) is 48.9 times a round trip's 0.19 %. The book's Sharpe is 0.92, 0.35 above holding the coin. It fails on mean daily return (0.00044 against 0.0005) and Calmar (0.68 against 0.75), which fits the skewed, year-driven returns of F1 and F2.

## Ideas
- `021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins` (from F1, F4, F5, F7): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 26 days, and the thinner the cloud at the cross, measured as its width relative to price, the larger the rise.
- `021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall` (from F3, F5, F6, F7): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 26 days, and the more the coin fell over the past 26 days before the cross, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
