---
line: 7.c no effect
backtest: 041-01.b1.b1_rise-continuation-more-coins_1d
idea tested: 041-01.b1.b1_rise-continuation-more-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3849 USD
---
## Findings
- **F1:** In the rising agitated profile, the tested continuation after large scaled rises is not there: rises above 1 standard deviation of the last 30 daily returns are followed by a next-day excess of +0.53 % (t 0.48, 64 cases, 51 days). The slope on the rising side is +0.85 % per standard deviation (t 1.35, 240 cases). The sign flips by year, from −1.49 % in 2020 (23 cases) to +2.05 % in 2021 (33 cases). Step 5's forecast-weighted t is 0.81.
- **F2:** What the market does instead after a small up day in the rising agitated profile is give it back. A rise of 0 to 0.5 standard deviations is followed by a next-day excess of −1.53 % (t −2.74 with one day's cases together, 111 cases, 96 days). Rises of 0 to 1 standard deviation have a negative mean excess in 19 of the 22 horizon-and-offset grids from 1 to 7 days. Both main coins show it (BCH −0.78 %, t −1.38; ZEC −0.98 %, t −1.56).
- **F3:** Large scaled falls in the rising agitated profile do not rebound but keep falling over the next days. After a fall below −1 standard deviation, the next-day excess is −0.58 % (t −0.58, 59 cases). Over 5 days it is −6.53 % (t −1.71, 15 cases, 10 days) and over 7 days −7.39 % (t −2.00). The mean is negative in 18 of 22 horizon-and-offset grids. BCH is clearest at −11.2 % over 5 days (t −2.32), against ZEC at −4.20 % (t −1.18).
- **F4:** The brief's next-day rebound after a fall exists outside the rising agitated profile, not inside it. Outside the profile, falls of −2 to −1 standard deviations are followed by +1.65 % the next day (t 3.12, 154 cases), and falls below −2 by +2.35 % (t 2.22, 34 cases).
- **F5:** The tested idea's move is far below the cost of trading it, while the reversals in F2 and F3 are larger than that cost. Per case the total move is +0.23 % and the unusual move +0.12 % (t 0.44, 529 days), against 0.37 % per trade. The book earns −0.1 % a year with a Calmar of −0.002. By contrast, the moves in F2 (−1.5 % in a day) and F3 (−6 % over 5 days) are several times the cost.

## Ideas
- `041-01.b1.b1.c1_agitated-rise-falls-keep-falling` (from F3, F4, F5): In a rising, agitated market, the larger a coin's one-day fall measured against the standard deviation of its daily returns over the last 30 days, the larger its further fall over the next five days.
- `041-01.b1.b1.c2_weak-up-day-giveback-short` (from F2, F1, F5): In a rising, agitated market, a coin's one-day rise that is small against the standard deviation of its daily returns over the last 30 days is given back over the next three days, and the fall is larger the smaller that scaled rise is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
