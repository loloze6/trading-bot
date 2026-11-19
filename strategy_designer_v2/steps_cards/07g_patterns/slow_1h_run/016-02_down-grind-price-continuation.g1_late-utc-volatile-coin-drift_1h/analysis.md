---
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
idea tested: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3284 USD
---
## Findings
- **F1:** The 21:00–23:00 UTC rise the tested idea uses is real in the bars and broad. The hour starting 20:00 averages +5.45 bp (t 6.75, n 17403) and the hour starting 21:00 averages +4.36 bp (t 5.66). Together the two hours are positive in all 6 coins (+4.2 to +5.5 bp, t 2.98 to 4.44) and in 7 of 8 years; the exception is 2022 (−2.18 bp, t −1.44).
- **F2:** The book loses because its fees are larger than its gross gain, not because the slot drift is absent. Summed per-bar gross gains are positive for every coin (+0.98 to +1.69), while summed fees are larger for every coin (2.53 to 3.49). The book only earns in the 20:00 and 21:00 bars (+1.96 and +2.49 bp per bar on average).
- **F3:** A large one-day fall is followed by a rebound over the next day. On non-overlapping 24-hour samples, the lowest fifth of past-day return scaled by 7-day hourly volatility is followed by a mean +55 bp next day (t 5.56, n 3251). The other four fifths range from −6.7 to +5.5 bp, all with |t| < 0.8. On raw past-day return the lowest fifth gives +59 bp (t 5.54).
- **F4:** Over three days, moves continue. The next 3-day vol-scaled return regressed on the past 3-day vol-scaled return has slope +0.072 (t 4.15, n 5251), and the slope is positive in all 6 coins (t 0.48 to 2.50). The top fifth of past 3-day moves is followed by +115 bp over the next 3 days (t 4.14, n 1053).
- **F5:** Several hour and weekday effects are weaker than the slot drift or do not hold across years:

## Ideas
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.g1_one-day-crash-rebounds` (from F3): When a coin has fallen sharply over the past day relative to its usual hourly volatility, it rises over the next day. The deeper the volatility-scaled 1-day fall, the larger the next-day rebound.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.g2_three-day-move-continuation` (from F4): A coin's volatility-scaled 3-day return continues in the same direction over the next 3 days. The larger the past 3-day move relative to its 7-day hourly volatility, the larger the move that follows, most clearly after strong rises.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.g3_evening-slot-drift-strength` (from F1, F2): Each coin rises over the two hours from 21:00 to 23:00 UTC, and the rise held on a day is larger when the coin's daily drift over the past 30 days has been higher, so that the slot gain is large enough per trade to matter.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
