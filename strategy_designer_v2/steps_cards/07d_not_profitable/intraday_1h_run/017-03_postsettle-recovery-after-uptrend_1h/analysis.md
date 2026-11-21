---
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend_1h
idea tested: 017-03_postsettle-recovery-after-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4980 USD
---
## Findings
- **F1:** Fees, not direction, sink the book: the position earns 0.000458 a coin-day before costs but pays 0.001714 a coin-day in fees, on a turnover of 1.61 book units a day (about 10.7 bp per unit traded); the daily book returns −0.001259 while holding the coins returns +0.001190 (32,163 trades, median 120 minutes, mean −0.164 % gross and −0.264 % net, t −19.95).
- **F2:** The 2-hour post-settlement move is too small to pay a round trip: on up-trend entry bars the 2-bar excess return is only −0.7 to +5.4 bp across the 72-bar-rise quintiles, and its mean is 2.3 bp across the 24 windows (between −10.0 and +19.6). A round trip costs about 21 bp per unit of book.
- **F3:** Only the 16:00 UTC settlement carries the effect. With a positive 3-day rise, entries at the 15:00 bar earn an excess of 9.8 bp over 2 bars (t 6.17), 21.6 bp over 8 bars (t 7.46) and 19.7 bp over 16 bars (t 4.88), all from about 8,580 cases. At the 23:00 bar the excess is 2.1 bp over 2 bars (t 1.26) and −1.9 bp over 8 bars (t −0.68).
- **F4:** The 08:00 UTC settlement runs the other way: up-trend entries at the 07:00 bar lose 3.7 bp over 2 bars (t −2.46) and 11.4 bp over 8 bars (t −3.86, 8,678 cases). At the book level the 07:00 bar costs 2.6e-4 in fees a coin-day for −4.3e-5 of gross gain.
- **F5:** At 16:00 the 8-hour move is graded by the 3-day rise. Across the 72-bar-rise quintiles at the 15:00 bar, the 8-bar excess rises from −0.5 bp in the middle quintile to 14.4 bp (t 3.76) and 37.6 bp in the top quintile (t 6.62). The slope t on up-trend cases is 4.60, and the top quintile still holds 29.0 bp over 24 bars (t 3.05).
- **F6:** A clock time with no settlement shows no such move: up-trend entries at the 11:00 bar give an 8-bar excess of 2.9 bp (t 0.89, 8,654 cases).

## Ideas
- `017-03_postsettle-recovery-after-uptrend.d1_16-00-settlement-eight-hour-recovery` (from F1, F2, F3, F5, F6): For a coin with a strong 3-day run up, the return over the 8 hours after the 16:00 UTC funding settlement (measured from the close of the hour before it) is positive, and the stronger the 3-day rise, the larger that post-settlement recovery. This holds only at the 16:00 UTC settlement, not at 00:00 or 08:00.
- `017-03_postsettle-recovery-after-uptrend.d2_08-00-settlement-uptrend-giveback` (from F4): For a coin with a strong 3-day run up, the return over the 8 hours after the 08:00 UTC funding settlement (measured from the close of the hour before it) is negative, and the stronger the 3-day rise, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
