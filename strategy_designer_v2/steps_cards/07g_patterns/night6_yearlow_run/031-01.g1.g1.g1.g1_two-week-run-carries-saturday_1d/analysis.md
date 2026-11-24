---
line: 7.g patterns
backtest: 031-01.g1.g1.g1.g1_two-week-run-carries-saturday_1d
idea tested: 031-01.g1.g1.g1.g1_two-week-run-carries-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4639 USD
---
## Findings
- **F1:** The tested effect belongs to Friday alone: the slope of the next day's excess return on the 14-day volatility-scaled run is 0.00561 (t 2.87, 2178 cases, 363 days) when the signal is taken at Friday's close, while on the other six weekdays its t lies between −0.54 and 1.29.
- **F2:** The book's Saturday gain comes almost entirely from its long side. Friday long positions earn a mean 0.616 % per position (1071 positions); short positions earn 0.007 % (1069). By Friday run quintile, the Saturday excess is +1.03 % in the top quintile (t 2.75, 436 cases), against −0.34 % (t −0.99) and −0.20 % (t −0.96) in the two bottom quintiles.
- **F3:** A one-day move reverses on the next day when volatility is high. In the top third of 20-day volatility relative to the coin's median, the slope of the next-day excess on the day's move in usual daily moves is −0.00664 (t −3.57, 5085 cases), and −0.00552 (t −1.93) over two days on a non-overlapping grid. In the low-volatility third it is +0.00117 (t 1.40).
- **F4:** The reversal is mostly a rebound after down days. Over all days the reversal slope is −0.00195 (t −2.31, 15220 cases, 2538 days). On down days it is −0.0039 (t −1.80); on up days it is +0.0009 (t 0.76). The bottom quintile of one-day moves is followed by a next-day excess of +0.41 % (t 2.26, 3039 cases). XMR shows the reversal most strongly (t −4.12).
- **F5:** Distance from the low or high of the past 60 days predicts neither the next day nor the next 5 days (t 0.46 and 0.60 from the low; −1.04 and −0.98 from the high). Nothing in the bars supports the brief's near-the-low story in either direction.
- **F6:** Saturday carries all of the book's gain and all of its falls. Saturday book days sum to +0.924 against +0.735 overall, the difference being the Friday trading cost of −0.046 % per day. The five worst Saturdays average −3.69 %, and the worst tenth of Saturdays average −1.82 %, with near-zero prior 14-day runs (mean 0.02).

## Ideas
- `031-01.g1.g1.g1.g1.g1_volatile-day-drop-rebounds-next-day` (from F3, F4): In a high-volatility regime, the larger a coin's fall over the past day, measured in its usual daily moves, the more it rises over the next day.
- `031-01.g1.g1.g1.g1.g2_friday-rise-carries-saturday-long` (from F1, F2, F6): The larger a coin's 14-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
