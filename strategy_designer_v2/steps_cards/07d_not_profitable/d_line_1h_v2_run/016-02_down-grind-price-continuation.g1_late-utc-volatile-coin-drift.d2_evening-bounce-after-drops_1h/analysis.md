---
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
idea tested: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3621 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: the 7,153 trades average a gross gain of 0.0083 (t 0.47, 52.3% winners) against a fee of 0.100, leaving -0.092 net per trade; across all bars the held position earns 1.3e-5 per bar gross while fees cost 1.9e-5 per bar, so the daily book return is -0.000143 while holding the coins earns +0.00119.
- **F2:** The bounce the book trades is smaller than one round trip even where it is strongest: at the 21:00 bars, the excess 2-hour return is 0.00179 (t 4.58, n 2112) in the deepest-fall quartile and only 0.00126, 0.00064 and 0.00105 in the next three; the book's fee per position is about 0.0011 at entry (0.000224 per hour-20 bar against 41% of those bars in a position at a mean size of 0.51) and about as much again at exit.
- **F3:** Part of the 2-hour rise is the clock, not the fall: every 20:00-bar close shows an excess 2-hour return of 0.00085 (n 17,403), the largest of any hour, and 21:00 bars after no fall still show 0.00047 (t 3.29, n 8525), so the fall's added value over 2 hours is only about 0.0005 to 0.0013.
- **F4:** The 2-hour gain is not graded the way the forecast assumes: the top entry-forecast quintile (mean forecast 19.8) grosses -0.0067 per trade while the fourth quintile (14.2) grosses +0.120 and the bottom two lose about -0.036 each, so sizing up the deepest falls adds fees without adding gain.
- **F5:** Over a full day after the 21:00 close the fall's effect is graded and large: the excess 24-hour return is +0.00218 (t 1.93) in the deepest-fall quartile, +0.00072 in the second, -0.00091 in the third, -0.00188 (t -1.80) in the shallowest and -0.00086 (t -1.70) after no fall, so the spread is about 0.004, roughly twice a round-trip fee.
- **F6:** Across every hour of the day, the deepest quarter of vol-scaled 24-hour falls is followed by a positive excess 24-hour return at 23 of 24 hours, from 0.0050 to 0.0068 at hours 0 to 5, against 2-hour excesses that change sign from hour to hour (-0.0012 to +0.0024).
- **F7:** The loss is spread over the whole period, not held in one window: gross position gain is positive in 19 of 24 windows, yet fees exceed gross in 17 of them, and the lowest Sharpe with one window left out is still -0.90.

## Ideas
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.d1_evening-fall-next-day-rebound` (from F1, F2, F5, F7): Each coin rises over the 24 hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.d2_vol-scaled-fall-daily-rebound` (from F5, F6, F1): A coin rises over the next 24 hours after a fall over the past 24 hours, and the larger that fall measured in units of its 7-day hourly volatility, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
