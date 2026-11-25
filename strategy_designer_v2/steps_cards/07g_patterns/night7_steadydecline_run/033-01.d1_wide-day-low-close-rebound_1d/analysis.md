---
line: 7.g patterns
backtest: 033-01.d1_wide-day-low-close-rebound_1d
idea tested: 033-01.d1_wide-day-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4128 USD
---
## Findings
- **F1:** The tested idea's effect lives mostly in falling, agitated markets. There, the top fifth of the close-near-low × wide-day measure is followed by a next-day excess return of +1.64 % (t 2.23, 263 cases). In falling calm markets the same top fifth gives −0.25 % (t −0.41, 177 cases), in choppy calm −0.33 % (89 cases) and in rising agitated −0.17 % (168 cases); only rising calm comes near, at +0.88 % (t 1.78, 186 cases).
- **F2:** The rebound needs the wide day. A close in the bottom fifth of the day's range gives +1.28 % the next day on days in the widest range tercile (t 3.15, 588 cases), +0.64 % in the middle tercile (t 1.71) and −0.37 % on narrow days (t −0.84, 416 cases).
- **F3:** The effect is one day long. The top fifth of the close-near-low × wide-day measure gives +0.67 % on the next day (t 2.36, 1,452 cases) and −0.05 % on the day after (t −0.18), and a bottom-fifth close gives only +0.28 % over 3 days (t 0.74).
- **F4:** The mirror is absent. The top fifth of the close-near-high × wide-day measure is followed by −0.16 % (t −0.64, 1,455 cases), against +0.14 % for its bottom fifth (t 0.56).
- **F5:** The close's place in the range cannot be told apart from the day's own fall. In a joint regression with day clusters, the close's nearness to the low gets t 1.12, the day's return in units of its 20-day swing gets t −0.88, and the range multiple gets t 1.27. A close in the lower half after a day in the lowest return tercile gives +0.49 % (t 2.10, 2,142 cases), while a close in the lower half after a mid-tercile day gives +0.14 % (t 0.58).
- **F6:** The book is mostly a long-the-coin book carried by its tail days. Its daily returns correlate 0.82 with the coins' and its mean position rises from 0.07 to 0.81 across the measure's quintiles. Without its best 2 % of days (29 days, mean +6.72 %), the sum of its daily returns falls from +166.6 % to −28.2 %.
- **F7:** Over all bars the idea is too small to pay. The unusual move is +0.09 % per case (t 0.81) against a trade cost of 0.19 %. The falling-agitated cases of F1, at +1.64 % each, are about 8.6 times that cost.

## Ideas
- `033-01.d1.g1_falling-agitated-low-close-rebound` (from F1, F2, F3, F7): In a falling, agitated market, the nearer a coin's daily close sits to that day's low, and the wider that day's high-low range against its usual daily range over the past 20 days, the larger the rise in its price over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
