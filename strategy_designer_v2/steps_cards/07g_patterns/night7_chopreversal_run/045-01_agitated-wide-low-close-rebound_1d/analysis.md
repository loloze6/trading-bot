---
line: 7.g patterns
backtest: 045-01_agitated-wide-low-close-rebound_1d
idea tested: 045-01_agitated-wide-low-close-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3947 USD
---
## Findings
- **F1:** The tested effect sits in the falling, agitated profile. There, the next day's demeaned return rises with the idea's product (low close × range width) with a slope of 0.0290 and t 3.68 (738 cases, 229 days). In the rising agitated profile it is flat (slope 0.0058, t 0.71, 755 cases), and in every calm profile |t| ≤ 0.48 (517 to 1164 cases each).
- **F2:** Inside the falling, agitated profile the reward sits in the top fifth of the product: +2.26 % next day (t 2.25, 148 cases). The other four fifths range from −1.14 % to +0.02 % (all |t| < 1.9). So the move per case in that top fifth is about 12 times the 0.19 % cost of a trade.
- **F3:** The falling-agitated slope is positive on every coin. It is above t 2.5 on five coins (BTC t 4.61, ETH 2.55, LTC 3.05, XMR 3.11, XRP 6.71) and weaker on ZEC (t 1.40). ZEC is also the only coin whose trades lose on average (−0.29 % net, 570 trades).
- **F4:** The falling-agitated slope is positive in all four windows with enough cases: w14 t 1.88, w15 t 1.59, w16 t 5.12, w18 t 0.59.
- **F5:** The effect lasts one day only. On a non-overlapping 2-day grid, the falling-agitated slope turns to −0.0079 (t −0.54, 363 cases), against t 3.68 at one day.
- **F6:** In agitated markets the next day falls steadily as the close moves up the range. By quintile of close location, low to high, the next day is +0.88 % (t 2.25), +0.26 %, −0.18 %, −0.37 % and −0.58 % (t −1.83), about 700 to 770 cases each. An up day that closes in the upper half of its range is followed by −0.55 % (t −2.30, 1601 cases).
- **F7:** Range width does not sharpen the high-close side. In agitated markets, a top-quintile close is followed by −0.66 % on narrow days (t −1.26), −0.70 % on mid days (t −1.67) and −0.30 % on wide days (t −0.58). The low-close side does grow with width: −0.02 %, +0.97 % (t 1.50) and +1.77 % (t 2.59).
- **F8:** In the falling, agitated profile the day's own return predicts the next day more strongly than the close location does. The slope is −0.289 (t −4.40, 738 cases). By quintile of the day's return, the lowest fifth is followed by +2.77 % (t 2.71) and the highest fifth by −1.36 % (t −2.06). The rising agitated profile shows nothing (slope +0.052, t 0.93).
- **F9:** The book's gain comes from short holds. Trades of up to 1.5 days earn +2.39 % on average (1002 trades), while trades of 1.5 to 7 days earn +0.01 % (749 trades) and −0.96 % (494 trades).

## Ideas
- `045-01.g1_falling-agitated-low-close-rebound` (from F1, F2, F3, F4, F5, F9): In a falling, agitated market, the lower a coin closes within its day's high-low range, and the wider that range is against its usual daily range over the past 30 days, the larger its rise over the next day.
- `045-01.g2_agitated-high-close-next-day-fade` (from F6, F7): In an agitated market, the higher a coin closes within its day's high-low range, the larger its fall over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `045-01.g3_falling-agitated-one-day-reversal` (from F8, F5): In a falling, agitated market, the larger a coin's one-day fall, the larger its rise over the next day, and the larger its one-day rise, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
