---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4184 USD
---
## Findings
- **F1:** Across the 6 coins, a coin's 1-day return counted in its usual 1-day move predicts the next day the other way. The bottom decile of that return is followed by an excess of +0.55 % over the next day (strength 0.105, t 3.64, 1638 independent cases) and the second decile by +0.28 % (strength 0.060, t 2.36, 1535 cases). Deciles 6 to 9 are followed by −0.19 % to −0.21 % (strength −0.040 to −0.049, t −1.4 to −2.1). The correlation of the 1-day z-return with the next day's z-move is negative on every coin (−0.019 BTC to −0.103 XMR). Before costs, then, the move is graded.
- **F2:** The rebound after the 1-day falls in the bottom two deciles has the same sign on all 6 coins, though no coin reaches t 2.6 on its own: +0.18 % BTC (t 1.06), +0.22 % ETH (t 0.96), +0.49 % LTC (t 1.97), +0.52 % XMR (t 2.31), +0.59 % XRP (t 2.50) and +0.52 % ZEC (t 1.91), against round trips of about 10 to 31 bps. By year, 7 of 8 years are positive, and 2022 is flat (−0.02 %, t −0.14).
- **F3:** The same rebound is about 2.5 times larger while the coin's 7-day return is positive: +0.71 % over the next day (strength 0.142, t 5.03, 984 cases), against +0.28 % (strength 0.057, t 2.28, 2189 cases) when the 7-day return is negative. Measured over 3 days, the bottom decile of the 1-day z-return is followed by +1.18 % (strength 0.128, t 3.08, 538 cases).
- **F4:** The 4-hour bar sorts the same way. Its bottom decile of return is followed by +0.42 % over the next day (strength 0.081, t 2.49, 1796 cases), and deciles 7 to 9 by −0.16 % to −0.21 %. A raw 1-day return in its bottom quintile gives +0.57 % (strength 0.117, t 5.94, 3523 cases).
- **F5:** Closes below the 2-day low are followed by gains over the next 3 days, not losses:
- **F6:** The book's worst days are the coins' falls. Its bottom 5 % of days lose 6.09 % against the coin's 6.00 %, after a coin day of +2.33 % before them. The next coin day is +0.86 %, which fits the 1-day rebound in F1.
- **F7:** Two other patterns are weaker or not stable:

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges.g1_one-day-fall-rebounds-next-day` (from F1, F2, F4, F6): The further a coin's close has fallen over the past day, counted in the coin's usual one-day move, the more the coin rises over the next day.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges.g2_dip-in-rising-week-rebounds` (from F1, F3): While a coin's 7-day return is positive, the further its close has fallen over the past day, counted in its usual one-day move, the more it rises over the next one to three days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges.g3_deep-downside-break-reverses` (from F5, F1, F3): While a coin's 7-day return is negative, the further a four-hour close sits below the lowest low of the preceding two days, counted in the coin's 30-day average four-hour range, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
