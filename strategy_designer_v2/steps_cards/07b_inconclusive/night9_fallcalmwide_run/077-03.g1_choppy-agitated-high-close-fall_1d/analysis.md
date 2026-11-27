---
line: 7.b inconclusive
backtest: 077-03.g1_choppy-agitated-high-close-fall_1d
idea tested: 077-03.g1_choppy-agitated-high-close-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2281 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts, with a next-day unusual move in the short direction of +0.79 % per case (t 3.26, 538 cases on 355 days), but the supporting check fails: the larger-|forecast| half is 0.18 % worse than the smaller half; in folds B and C the 126 cases (96 days) average +1.31 % (t 1.77).
- **F2:** The day's width against the 30-day swing carries the effect: among the cases, the widest third gives +3.38 % (t 2.17, 33 cases, 27 days), while the middle and narrowest thirds give -0.20 % (t -0.17) and +0.68 % (t 0.62).
- **F3:** Closeness to the high grades the wrong way, and it dilutes the forecast:
- **F4:** The effect holds across years in folds B and C (2019 +1.95 %, 2020 +1.99 %, 2021 +0.64 %, 2018 +0.05 % on 9 cases), and on the main coins it is positive on BTC (+3.35 %), ETH (+2.01 %) and ZEC (+1.73 %) and near zero on LTC, XMR and XRP. It is uneven by coin, not tied to one period.
- **F5:** The mirror side shows the same reversal. In the profile, closes in the bottom quarter of the range are followed by rises: in the short direction, -2.14 % (t -1.82, 40 cases) for closes 75–90 % down the range and -1.03 % (t -1.55, 34 cases) for the bottom tenth. A near-high close on a day whose return was in the lowest third falls the most (+3.04 %, t 2.06).
- **F6:** Size against cost: the total move of +0.67 % per case is 3.0 times the 0.22 % cost of a trade. The book still lost to holding (Sharpe 0.52, 0.03 below holding's) because it was in a position on only 3 % of coin-days.

## Ideas
- `077-03.g1.b1_choppy-agitated-wide-high-close-fall` (from F1, F2, F3, F4): In a choppy, agitated market, a day closing near its high falls over the next day, and the fall is larger the wider the day's range against the coin's 30-day swing of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
