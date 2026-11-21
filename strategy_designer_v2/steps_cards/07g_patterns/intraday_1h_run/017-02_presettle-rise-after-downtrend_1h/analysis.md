---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend_1h
idea tested: 017-02_presettle-rise-after-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3956 USD
---
## Findings
- **F1:** The two hours held through 21:00–22:00 UTC carry a clear positive excess. The next-bar excess is +4.83 bp (t 5.98) for the hour held at 21 and +3.74 bp (t 4.85) for the hour held at 22. Measured once per day from the 20:00 bar, the 2-hour excess is positive in every coin: +7.3 to +9.6 bp, t 2.6 to 4.1, about 2,900 cases each. It is positive in 74% of 144 coin-windows and in 7 of 8 years; the exception is 2022 (−5.5 bp, t −1.83).
- **F2:** Inside that 21:00–22:00 UTC window, the 2-hour gain is larger after a deeper 24-hour fall. Its slope on the 24-hour z-score is negative in all six coins, from −0.9 to −11.6 bp per z. It reaches t −3.93 in LTC with 2,199 cases; the other coins lie between t −0.27 and −1.64.
- **F3:** A coin's next hour reverses its last hour, and the reversal grows with the size of the move. The next-hour excess slope on the last hour's volatility-scaled move is negative in all six coins, from −0.69 to −4.21 bp per z, t −1.7 to −7.0, about 52,000 bars each. Buckets run from +14.2 bp (t 3.38) after moves of −3 z or worse to −3.3 bp (t −4.29) after moves of +1 to +2 z.
- **F4:** The one-hour reversal sits in high-volatility periods. Its slope is −5.19 bp per z (t −10.1) in the top quintile of 24-hour volatility, against +0.44 bp (t 1.19) in the lowest quintile and −0.6 to −0.9 bp in the middle quintiles.
- **F5:** A coin's next 24 hours reverse its last 24 hours. On non-overlapping daily cases, the slope on the 24-hour z-score is negative in all six coins, from −16.8 to −35.0 bp per z, t −1.76 to −3.34, about 2,170 cases each. The lowest 24-hour z quintile is followed by +47.1 bp (t 4.36) and the highest by −24.7 bp (t −2.49).
- **F6:** Some clock hours are reliably weak:
- **F7:** The tested 3-day-fall grading is not there, and fees decide the book:

## Ideas
- `017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall` (from F1, F2): Over the next 2 hours from the 21:00 UTC bar, a coin's return is positive, and the deeper its 24-hour fall, the larger that late-evening rise.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods` (from F3, F4): Over the next hour, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly when the coin's 24-hour volatility is high.
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal` (from F5): Over the next 24 hours, a coin moves against its 24-hour return, and the larger that return relative to the coin's usual volatility, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
