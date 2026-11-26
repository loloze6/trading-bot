---
line: 7.g patterns
backtest: 061-01.g1.g1_big-up-day-continues_1d
idea tested: 061-01.g1.g1_big-up-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5611 USD
---
## Findings
- **F1:** The tested long-only signal pays only through the coin's own drift: its cases have an unusual 5-day move of -0.26 % (t -0.84, 1179 days), the book's daily returns correlate 0.82 with the coins' and it holds a position on 92 % of coin-days, so its Sharpe of 0.64 is mostly holding the coin.
- **F2:** In a calm market (30-day swing at or below the coin's median), the day's move in swing units, read in its own direction, is followed by an unusual 5-day move of +1.39 % (t 2.47, 713 cases, 174 days; weighted by the day's size +1.79 %, t 2.66). In an agitated market it is +0.40 % (t 0.55, 709 cases, 211 days).
- **F3:** The calm-market follow-through of F2 does not hold on every 5-day grid offset. Over the five offsets the signed unusual move is +1.39 %, +0.36 %, +0.69 %, -0.38 % and +0.89 % (t from -0.65 to 2.47). In agitated markets it is +0.40 %, -1.16 %, +0.24 %, -0.12 % and -0.26 %. So calm is above agitated on all five offsets, but the calm effect alone is weak outside offset 0.
- **F4:** The calm-market follow-through is spread across coins and years rather than coming from one of them. It is positive on 5 of 6 coins (XMR +2.69 %, t 3.70; ETH -0.03 %) and in 3 of 4 years (2019 +2.62 %, t 2.68; 2021 +2.62 %, t 2.14; 2020 -0.56 %). On days larger than 1.5 swings it is +3.67 % on offset 0, against -0.18 % in agitated markets.
- **F5:** The size of the day grades the next 5 days on the up side when no profile is applied. Days above +2 swings are followed by +6.49 % unusual (t 2.52, n 38) and days of +1 to +2 swings by +1.81 % (t 1.71). In a rising market large up days are followed by +8.38 % (t 2.15, n 29) and in a falling market by +0.10 % (n 13). Rising-market continuation is already held on the map (034-01.e1, 034-02).
- **F6:** In an agitated market a day below -2 swings is followed by a next-day rebound of +4.29 % (t 2.74, n 68) and a day of -2 to -1 swings by +1.21 % (t 1.92). In a calm market the same days are followed by about +0.25 % (t 0.28). This agitated-fall rebound is already held on the map (044-02, 047-01, 051-01), so it is not a discovery.
- **F7:** Other angles showed nothing beyond chance once same-day cases were pooled and grid offsets were checked:

## Ideas
- `061-01.g1.g1.g1_calm-big-day-follow-through` (from F2, F3, F4, F1): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further the coin keeps moving the same way over the next 5 days, up after up days and down after down days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
