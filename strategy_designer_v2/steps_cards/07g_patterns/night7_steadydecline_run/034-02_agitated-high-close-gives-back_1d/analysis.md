---
line: 7.g patterns
backtest: 034-02_agitated-high-close-gives-back_1d
idea tested: 034-02_agitated-high-close-gives-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3754 USD
---
## Findings
- **F1:** In agitated bars the reversal lives on the low side: closes in the lowest fifth of the day's range were followed by a next-day excess return of +0.88 % (t 2.24, 732 cases), while closes in the highest fifth were followed by −0.58 % (t −1.83, 769 cases). The long side's move per case is about 4.6 times the 0.19 % cost of a trade, far above the tested short book's +0.07 % total move.
- **F2:** Agitation matters. The next-day excess return, in units of the coin's 20-day swing, rises with how low the close sits in the range: slope 0.293 (t 2.74, 3,333 cases) in agitated bars against 0.092 (t 0.71, 4,307 cases) in calm bars. The slope is positive on all six coins in agitated bars (0.20 to 0.52; XMR t 3.68, ETH t 2.34).
- **F3:** Inside agitated bars the low-close reading depends on the 60-day trend. It holds in falling markets (slope 0.597, t 2.72, 738 cases) and choppy ones (1.375, t 2.03, only 120 cases), and is absent in rising ones (−0.149, t −0.71, 755 cases). The short side the book traded is therefore mostly taken in the wrong place.
- **F4:** Combining a low close with the size of the day's fall (low-close share × the fall in units of the 20-day swing) predicts the next day best. Its slope is 0.229 (t 3.26) in agitated bars and 0.040 (t 0.42) in calm bars. On agitated down days, the largest quarter of falls was followed by +1.53 % (t 2.38, 412 cases); the three smaller quarters were followed by +0.19 % to +0.41 % (t under 0.9).
- **F5:** The size of the day's own fall, apart from where the day closed, predicts a next-day rebound in falling agitated bars: slope 0.216 (t 3.48, 738 cases). It does not in rising agitated bars (−0.043, t −0.79) or in calm bars (0.004, t 0.11).
- **F6:** The effect is spent after one day. The low-close slope on the second day's return is −0.135 (t −1.28). Over a 3-day horizon the low-close quintiles show no order (t under 0.7).
- **F7:** The tested short book's gain came from few places. By coin it was carried by XMR (+0.185 % per position-day) and ZEC (+0.057 %), with BTC, ETH and LTC slightly negative. By year it was positive from 2018 to 2020 (+0.08 % to +0.14 %) and negative in 2021 (−0.104 %), the year with the most rising agitated bars.

## Ideas
- `034-02.g1_falling-agitated-low-close-rebound` (from F1, F2, F3, F6): In a falling, agitated market, the nearer a coin's daily close sits to the day's low within its high-low range, the larger its rise over the next day.
- `034-02.g2_deep-fall-low-close-rebounds` (from F1, F2, F4, F6): In an agitated market, the larger a coin's one-day fall relative to its usual daily swing and the nearer that day closes to its low, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `034-02.g3_outsized-agitated-fall-rebounds` (from F5, F4): In a falling, agitated market, the larger a coin's one-day fall relative to its usual daily swing over the past 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
