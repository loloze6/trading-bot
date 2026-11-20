---
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3192 USD
---
## Findings
- **F1:** The book loses before costs, so no change of fees fixes it: 17,075 trades, a median of 120 minutes each, average −0.064 % gross and −0.164 % net, only 46.9 % gross winners. The book's mean daily return is −8.4 bps.
- **F2:** The evening rise is too small to pay for a trade. The 20:00–22:00 move is 1.4 to 8.7 bps per case by coin, against a round trip of about 21 bps. Per case, the total move is 0.3 times the cost and the unusual move 0.2 times, in line with findings F2 and F11 of earlier runs.
- **F3:** The volatility grading lives only in the most volatile fifth of 7-day hourly volatility. There the 20:00–22:00 move is +19.1 bps (t 4.5, 3,334 cases). The other four fifths range from −0.7 to +2.6 bps (t below 1.6). So even its best cases stay below one round trip.
- **F4:** The evening move adds nothing to the rest of the day. The 22 hours after 22:00 return 4.9 to 8.8 bps in every volatility fifth, with t at most 1.2. In the top fifth that is 6.3 bps, no more than in the calm fifths.
- **F5:** Three-day moves made efficiently tend to continue (efficiency is the net 3-day return over the sum of its absolute hourly returns). In the most efficient fifth, the move continues by +91.6 bps over the next 3 days (t 3.3, 1,108 non-overlapping cases) and +104 bps over 7 days (t 2.3). That is 4.4 times a round trip.
- **F6:** The F5 effect is not graded across the middle fifths. Fifths 1 to 4 give +22, +0.3, +0.7 and −15.7 bps over 3 days, all |t| < 0.9. So the effect sits in the most efficient moves only.
- **F7:** The continuation of efficient moves is upward. After the most efficient rises, the coin gains +162 bps over 3 days. After the most efficient falls, it gains +9.6 bps, so a falling grind does not continue. The coin's normal 3-day drift is about +16 to +52 bps across volatility fifths.
- **F8:** Moves made with volume bunched into one hour lean toward giving back. Take the share of the past 3 days' volume traded in its biggest hour:

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising` (from F5, F6, F7, F2): The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves), the more it keeps rising over the next 3 days.
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_volume-burst-move-reverses` (from F8, F5): The larger the share of a coin's past 3-day volume traded in its single busiest hour, the more of its 3-day move the coin gives back over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
