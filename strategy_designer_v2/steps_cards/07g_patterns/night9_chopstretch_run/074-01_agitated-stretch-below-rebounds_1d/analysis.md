---
line: 7.g patterns
backtest: 074-01_agitated-stretch-below-rebounds_1d
idea tested: 074-01_agitated-stretch-below-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4105 USD
---
## Findings
- **F1:** The tested idea's depth does not grade the 10-day move in agitated markets: on the 10-day grid, unusual 10-day moves by depth below the 20-day average in usual moves are -2.00 % (t -0.93, n 66) below -2, +3.34 % (t 1.24, n 45) from -2 to -1 and +0.65 % (t 0.26, n 61) from -1 to 0. The 3-day moves are flat as well: -0.23 %, +0.09 % and -0.57 %, every |t| under 1.2. In agitated falling markets, stretches below the average average -0.02 % over 10 days (t -0.01, n 47).
- **F2:** In calm markets the stretch below the average is followed by further falls, and the effect lives in falling calm markets. There, on the 3-day grid, the unusual 3-day move is -2.93 % (t -4.21, n 148) below -2 usual moves, -2.25 % (t -2.30, n 67) from -2 to -1, and +0.96 % (t 1.14, n 59) from -1 to 0. The same bins in choppy and rising calm markets show no clear sign (-0.49 %, -2.88 %, -1.04 %, -0.92 %, all |t| under 1.5).
- **F3:** F2's continuation is not uniform over time. Calm stretches below -1 have a negative 3-day move in 8 of 12 windows, strongly in w9 (-1.76 %, t -3.01), w13 (-3.66 %, t -2.84), w14 (-5.25 %, t -3.00) and w15 (-2.74 %, t -2.47). Four windows are positive but small (w10 +0.23 %, w11 +0.92 %, w17 +1.63 %, w18 +1.29 %, all t under 0.8). Over all calm stretches below the average, the slope on depth is not significant (0.00205, t 0.50 clustered by day, 636 cases on 218 days), so the grading comes from the falling trend, not from depth alone.
- **F4:** In agitated markets, the higher a day closes in its own high-low range, the lower the next day's unusual return. The slope is -0.0186 per unit of close position (t -2.99 clustered by day, 3691 bars on 1051 days), against -0.0063 (t -1.48) in calm markets.
- **F5:** F4 is sharpest on wide agitated days. Among agitated days closing in the top fifth of their range, those whose range is widest against their 20-day average fall -1.43 % the next day (t -3.29, n 230), against -0.35 % (t -1.09) and +0.11 % (t 0.28) for narrower days. This high-close fall is negative in every year (2018 -1.47 %, 2019 -0.75 %, 2020 -0.30 %, 2021 -0.31 %) and on all six coins (-0.18 % to -1.03 %).
- **F6:** The low-close side of F4 is the known agitated rebound and is already held. In falling agitated markets, days closing in the lowest fifth of their range rise +2.23 % the next day (t 4.86, n 192). Agitated days falling more than 2 usual moves rise +3.99 % the next day (t 4.15, n 64). The map's 039-02, 044-01, 045-01 and 047-01 cover these, so they are no discovery.
- **F7:** The book earned the coin's drift, not the idea. Its trades' mean net result rises with the entry forecast, from -0.46 % to +5.16 %, but the median is flat at 4.1–4.6 % in every quartile. ZEC lost on average (-0.98 % over 212 trades) while BTC gained +3.10 %. The idea's unusual move is +0.05 % per case (t 0.06), 0.3 times one trade's cost of 0.19 %.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.g1_falling-calm-stretch-keeps-falling` (from F2, F3, F1): In a falling, calm market, the further a coin's close sits below its 20-day average, measured in units of the standard deviation of its daily returns over the same 20 days, the more it falls over the next 3 days.
- `074-01.g2_agitated-wide-high-close-fades` (from F4, F5, F6): In an agitated market, the wider a day's high-low range is against its range over the last 20 days, and the higher the day closes within that range, the more the coin falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
