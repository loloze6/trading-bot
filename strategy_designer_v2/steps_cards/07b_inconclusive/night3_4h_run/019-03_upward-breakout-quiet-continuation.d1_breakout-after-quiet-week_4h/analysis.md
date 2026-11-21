---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3394 USD
---
## Findings
- **F1:** The test could not measure its own grading, because the forecast is pinned at its cap: 87 % of the 3,101 bets enter at a forecast of 20, and the median, the 25th percentile and every quantile above them equal 20. The split at the median therefore left 0 cases in the high-forecast half and 3,102 in the low half, so the supporting check returned nothing.
- **F2:** The quietness of the past week is the part of the idea that does grade the move, though weakly. Over the 2,733 breakouts (first per 18-bar cell), those with the quietest 7-day/60-day range ratio (lowest quarter, below 0.77) end 18 bars later +0.69 % above drift (t 2.00, strength 0.087). The loudest quarter (above 1.15) ends −0.36 % (t −0.87, strength −0.059). The rank correlation of the ratio with strength is −0.068 (p 0.0004), and the slope on its within-coin rank is −1.27 % (t −2.16). The bets show the same pattern: quietest quarter +0.70 % (t 2.00, 661 cases), loudest −0.41 % (t −1.02).
- **F3:** The other two parts of the forecast predict nothing. The stretch's narrowness against the 30-day range has a rank correlation of 0.007 with strength (p 0.70), and the size of the break above the 12-bar high has 0.010 (p 0.61). Their multiplication only adds noise to the quiet-week factor.
- **F4:** The effect is mostly in the early years, which is why the overall t stays low. The bets' mean excess is +1.49 % in 2020 (t 3.67) but −0.87 % in 2019 (t −2.34) and −0.76 % in 2022 (t −2.05). The quiet-week gradient is clear in 2018-2021: quietest quarter +1.05 % (t 2.10) against loudest −1.56 % (t −2.35). In 2022-2025 it is absent: quietest +0.16 %, loudest +0.57 %.
- **F5:** Coins differ, and on its full cases the idea is too small to trade. Over all bets the move is +0.18 % above drift (t 1.13, 3,102 cases), 0.9 times the 0.19 % round-trip cost. By coin it ranges from LTC −0.54 % (t −1.56) to XRP +0.64 % (t 1.10). In the quietest-week quarter the unusual move is about +0.69 %, about 3.6 times the cost. On that quarter, five of the six coins are positive (XMR +1.34 %, t 2.15) and LTC is the exception at −0.45 %.
- **F6:** No other horizon shows the move more clearly. The bets' excess return is +0.02 % at 1 day (t 0.26), +0.03 % at 2 days (t 0.24), +0.18 % at 3 days (t 1.13) and +0.23 % at 6 days (t 1.05).

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins` (from F5, F4): When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days. The rise is larger the narrower that stretch was compared with the coin's 30-day average four-hour range, and larger still the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week` (from F2, F3, F1, F5): When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
