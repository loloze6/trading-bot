---
line: 7.b inconclusive
backtest: 031-02_extreme-fall-partly-rebounds_1d
idea tested: 031-02_extreme-fall-partly-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3530 USD
---
## Findings
- **F1:** The main measure is zero, not merely short of the bar: the 52 in-regime 30-day grid cases on 29 days have a mean excess return of +0.02 % (t 0.006); only 44 % beat the coin's mean, and the same cells read at 10, 20, 45 and 60 days give means of +0.8 %, +2.0 %, +2.9 % and −1.8 %, with no t above 0.76.
- **F2:** The cases split by what the coin did in the last 30 days: in-regime grid cases whose 30-day return was still negative averaged +3.2 % excess (25 cases, 14 days, t 0.47), and those whose 30-day return had already turned up averaged −8.4 % (11 cases, 5 days, t −1.67), so the two cancel in the main measure.
- **F3:** Every in-regime bar, read overlapping and so only descriptive, shows the same split: the three lower quartiles of the 30-day return (means −34 %, −19 %, −6 %) are followed by +9.3 %, +6.7 % and +10.7 % excess over 30 days, and the quartile already up 13 % by +1.2 %. By 10-day return, the up quartile gives −0.2 % against +6.5 % to +13.8 % for the others.
- **F4:** The still-falling part holds in every coin: in-regime bars with a negative 30-day return are followed by positive excess 30-day returns in all six coins (BTC +4.2 %, ETH +5.8 %, LTC +2.0 %, XMR +14.2 %, XRP +19.2 %, ZEC +7.4 %, 66 to 218 bars each). In-regime bars with a positive 30-day return are mixed (BTC −7.3 %, XMR −2.2 %, ZEC −1.7 %, the others positive).
- **F5:** The test could hardly see the gradient, because 73 % of the in-regime grid forecasts sit at the cap of 20: the forecast terciles give only −2.0 %, +0.3 % and +1.7 % excess (17 to 18 cases each), while the overlapping in-regime quartiles rise from +0.8 % to +4.7 % to +5.2 %.
- **F6:** The cases are few and bunched in time: 52 grid cases fall on only 29 days, and 2019 alone holds 10 cases at −8.7 %. The size measure's broader set (81 cases, 66 days) gives an unusual move of +8.21 % at t 1.49, 0.204 of a usual move, which is 42.5 times the 0.19 % cost of a trade. The effect, where it exists, is large against the cost but not yet told from 0.

## Ideas
- `031-02.b1_deep-fall-still-falling-rebounds` (from F1, F2, F3, F4, F6): The further a coin's 90-day return stands below its own usual 90-day move, measured against its own past volatility, the more its price rebounds over the next 30 days, only while its 30-day return is still negative.
- `031-02.b2_graded-deep-and-recent-fall` (from F2, F3, F5): The further a coin's 90-day return stands below its own usual 90-day move, measured against its own past volatility, the more its price rebounds over the next 30 days, and the rebound is larger the further its last 30-day return also stands below zero.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
