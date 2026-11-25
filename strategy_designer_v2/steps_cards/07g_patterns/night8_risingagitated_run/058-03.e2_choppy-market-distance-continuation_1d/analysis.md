---
line: 7.g patterns
backtest: 058-03.e2_choppy-market-distance-continuation_1d
idea tested: 058-03.e2_choppy-market-distance-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5792 USD
---
## Findings
- **F1:** Where a day closes in its own range predicts a reversal the next day, in steps: the next-day return minus the coin's normal drift falls by 0.321 % for each standard deviation of the close's position in the range (t -2.91, clustered by day, 8,688 cases on 1,448 days). By quintile of that position, the lowest closes are followed by +0.520 % (t 3.85, 1,729 cases) and the highest by -0.344 % (t -2.59, 1,735 cases).
- **F2:** The reversal lives in agitated markets and is absent in calm ones. The slope per standard deviation is -0.829 % in falling agitated markets (t -2.51, 1,252 cases) and -1.254 % in choppy agitated ones (t -2.63, 164 cases). It is -0.053 % in choppy calm (t -0.20), +0.148 % in falling calm (t 0.63) and -0.176 % in rising calm (t -0.82). In rising agitated markets it is +0.201 % (t 0.66), so it does not hold there.
- **F3:** The reversal grows with the day's width. In the widest third of days, a close in the upper half is followed by -0.418 % excess the next day (1,261 cases) and a close in the lower half by +0.892 % (1,285 cases). In the narrowest third the two are -0.150 % and +0.046 %. In falling agitated markets, the close position times the scaled range has a slope of -1.198 % per standard deviation (t -3.03, 1,252 cases, 333 days).
- **F4:** The reversal is broad. All six coins have a negative slope, from XRP at -0.136 % (t -0.76) to XMR at -0.667 % (t -4.85). Eleven of the 12 windows are negative; only w12 is positive, at +0.054 %.
- **F5:** The reversal fades within a day. Two days ahead, the close-position slope is -0.061 % in falling agitated markets (t -0.12) and -0.795 % in choppy agitated ones (t -0.82).
- **F6:** The tested idea is weak. The 20-day distance slope over 10 days in the choppy regime is +2.99 % per standard deviation (t 2.02 on only 126 grid cases, 63 days), and the official size is -0.03 % per case (t -0.06, 713 cases), against a trade cost of 0.19 %. The book's daily returns barely move with the coins' (correlation -0.067), and its window means range from -0.116 % to +0.260 % a day.
- **F7:** Next-day returns are highest on Thursday (+0.605 %, t 4.10, 1,242 cases) and Friday (+0.523 %, t 3.87, 1,231 cases). The gain is concentrated in rising markets (Friday +1.48 % on 225 cases, against -0.53 % in falling markets). This repeats the held idea 045-01, the rising market late-week gain, so it is already held and not proposed.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-03.e2.g1_agitated-wide-high-close-fades` (from F1, F2, F3, F4, F5): In a falling, agitated market, the higher a coin closes within a wide daily range (the closer its close to the day's high, and the wider the day against the coin's recent daily swing), the more it falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
