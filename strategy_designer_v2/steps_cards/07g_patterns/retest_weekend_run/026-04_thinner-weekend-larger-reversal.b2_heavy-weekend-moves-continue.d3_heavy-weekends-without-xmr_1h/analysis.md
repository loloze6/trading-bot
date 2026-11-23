---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3951 USD
---
## Findings
- **F1:** On weekends ending Sunday 23:00 UTC, the signed 48-hour move after the weekend (in usual 48-hour moves) grows with the log of the weekend-to-weekday volume ratio, with slope 0.187 and t 4.48 over 1904 cases. Windows ending on other weekdays show slopes of 0.015–0.064 with t of 1.8 or less, so the volume grading is specific to the weekend. By coin it holds in XRP (t 3.77), BTC (t 2.63), ETH (t 2.52) and LTC (t 1.93), but not in ZEC (t 0.18).
- **F2:** Inside heavy weekends (ratio above 1), the continuation does not grow with the size of the move: the slope on |move| is −0.070 with t −0.91 over 349 cases. The idea's size check failed because it graded by move size, not by volume (the size check came out at −0.0025). The volume ratio is what carries the effect.
- **F3:** The top volume-ratio quintile continues on both sides. Weekend rises go on by +0.257 usual moves over 48 hours (t 2.80, n 223) and weekend falls by +0.218 (t 2.34, n 158). The middle three quintiles sit near 0 (−0.012 to +0.095).
- **F4:** Weekend rises made on the thinnest volume (bottom ratio quintile, mean ratio 0.28) reverse over the next 48 hours: −0.205 usual moves, t −3.06, n 185. Weekend falls in the same quintile do not reverse (+0.023, t 0.35).
- **F5:** The hourly bars from 21:00 to 23:00 UTC rise on average by +0.049 % per hour (coins pooled per day, t 4.93, n 2920).
- **F6:** The 21:00–23:00 UTC rise grows with the coin's trailing 7-day volatility: +0.022 % per hour in the lowest tercile (t 3.34), +0.032 % in the middle (t 3.59) and +0.094 % in the highest (t 6.25). Only in the highest tercile does the two-hour move (about 0.19 %) reach the 0.17 % cost of a trade.
- **F7:** Hours 02:00–04:00 UTC were negative from 2018 to 2022 (t −4.51 to −1.26) and positive from 2023 to 2025 (t up to 2.11). This is a pattern that changes sign across years, so it supports no idea.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr.g1_weekend-volume-grades-continuation` (from F1, F2, F3): A coin's Saturday-Sunday move is followed over the next 48 hours by a move in the same direction, the larger the heavier its weekend volume is against its mean over the preceding five weekdays, whatever the size of the weekend move itself.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr.g2_thin-weekend-rises-reverse` (from F4, F1): A coin's Saturday-Sunday rise made on volume lighter than its mean over the preceding five weekdays is followed by a fall over the next 48 hours, the larger the thinner the weekend volume is against the weekdays.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr.g3_late-evening-utc-volatility-drift` (from F5, F6): A coin rises over the two hours from 21:00 to 23:00 UTC, the more the higher its volatility over the preceding 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
