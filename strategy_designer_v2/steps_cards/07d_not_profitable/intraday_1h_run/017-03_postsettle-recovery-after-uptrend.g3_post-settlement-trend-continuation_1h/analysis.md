---
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h
idea tested: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2824 USD
---
## Findings
- **F1:** The book loses because fees are larger than its gross gain: summed over all coins and windows, the gross position gain was 8.73 and the fees were 19.31, and every coin's fees exceeded its gross (for example XMR 0.71 against 3.69, BTC 1.59 against 3.17). Per daily 15:00 case, the gross was 0.000507 against 0.001102 in fees, and each of the roughly 3,500 trades per coin lasted a median of 120 minutes with a net mean of -0.18 % to -0.32 %.
- **F2:** The forecast is real and graded, but a 2-hour hold is too short to pay a round trip. Across 17,452 cases, the 2-hour signed excess return after the 15:00 bar was 0.000891, rising from 0.000448 in the weakest forecast quintile to 0.001852 in the strongest. Fees came to 0.00107 per unit of turnover, about 0.0021 per round trip, so every quintile lost net, between -0.00027 and -0.00076 per case.
- **F3:** The move with the 3-day trend keeps building well past the 2 hours after the 16:00 settlement. At the 15:00 bar, the mean signed excess return was 0.00087 over 2 hours (t 7.3, n 17,018), 0.00137 over 8 hours and 0.00157 over 12 hours. In the largest 3-day-return quintile, the 12-hour move reached 0.00259, above the roughly 0.0021 round-trip fee, against 0.00198 at 2 hours.
- **F4:** The 16:00 settlement is the hour where trend continuation is strongest. The 2-hour signed excess was 0.00087 (t 7.3) after the 16:00 close, against 0.00011 (t 1.1) after 04:00, -0.00020 (t -1.8) after 10:00 and 0.00037 (t 3.3) after 22:00. The 12-hour mean after 16:00 was positive in every coin and in 7 of 8 years for the 8-hour horizon.

## Ideas
- `017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation.d1_post-settlement-twelve-hour-trend-continuation` (from F1, F2, F3, F4): Over the 12 hours after the 16:00 UTC funding settlement, a coin moves in the direction of its own 3-day return, and the larger that 3-day return, the larger the move with it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
