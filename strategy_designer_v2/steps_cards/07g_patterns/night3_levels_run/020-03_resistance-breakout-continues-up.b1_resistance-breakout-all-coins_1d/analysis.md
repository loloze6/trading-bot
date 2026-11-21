---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4562 USD
---
## Findings
- **F1:** Closeness to the 60-day high orders the moves that follow, and the more so the longer the horizon. Over 5 days, cases in the top fifth of closeness (about 1066 per fifth) end +1.28 % above the coin's normal drift (t 2.4, strength 0.093). Over 10 days the five fifths run in order from the farthest to the nearest: −2.19 % (t −3.3), −1.39 %, −0.25 %, +1.08 %, +2.12 % (t 2.2, strength 0.116), with about 525 cases each. Over 20 days the rank correlation between closeness and the unusual move is positive in 15 of 19 coins (median 0.105). The top fifth's unusual move is 6 to 10 times the 0.22 % cost of a trade.
- **F2:** The strongest breaks through repeatedly held levels are followed by a fall over 20 days. On the 20-day grid, break bars in the top third of touch count × margin end −8.3 % below the coin's drift (t −3.9, 92 cases, strength −0.28). The lower two thirds end −1.7 % and −0.6 %. Over 20 days, break bars do worse than non-break bars in 15 of 19 coins (−3.5 % against +0.7 %).
- **F3:** The tested breakout's gain is short and fades. Break bars on the 5-day grid end +0.92 % above drift (t 2.0, 1265 cases); on the 10-day grid they end −0.35 % (t −0.4, 649 cases). Within the breaks, only the top quarter of touch count × margin is positive over 5 days (+1.3 %, t 2.3); the other three quarters are near 0.
- **F4:** The book's profit comes mostly from the coins' own rise rather than from timing. Its mean position is 0.48 of the book, held on 58 % of bars. Per case, the coins' normal drift (+0.74 %) is 2.5 times the unusual move (+0.29 %, strength 0.022).
- **F5:** The weekday on which a 5-day stretch starts goes with large differences: +2.40 % for Tuesday starts (t 4.4, 975 cases) and −1.58 % for Sunday starts (t −2.9). This is a weekday split on dates the coins share, from one look, and it gives no graded situation, so it is not used for an idea.
- **F6:** A large prior-day move and a strong 20-day return each show a positive top fifth over 5 days: +1.19 % (t 2.3) and +1.12 % (t 2.1). The other fifths are not in order (the second fifth is negative at t −2.3 and −2.4), so neither stands out from chance after this many angles.

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.g1_nearness-to-60-day-high` (from F1, F4): The closer a coin's close is to its highest close of the past 60 days, the more it rises over the next 10 days, above its normal drift.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.g2_strong-breakouts-reverse-later` (from F2, F3): When a coin closes above a price where it turned down several times in the past 90 days, the more times the level held and the further the close clears it, the more the coin falls over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
