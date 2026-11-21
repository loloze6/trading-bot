---
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
idea tested: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 3.7111 USD
---
## Findings
- **F1:** The book loses almost entirely to fees. Its mean daily gain before costs is +0.000066, against fees of 0.00278 a day, which leaves -0.00274 a day net. The fees come from turnover of 2.56 times the book per day at 0.00109 per unit turned over.
- **F2:** The forecast turns over far faster than the 24-hour effect it bets on. Its autocorrelation is 0.94 at 1 hour, 0.70 at 6 hours and -0.05 at 24 hours. Its slope on the next return is insignificant at 1 hour (t 1.44, 416,645 cases) and 6 hours (t 0.91, 69,355 cases), significant only at 24 hours (t 3.90, 17,246 cases), and gone at 72 hours (t -0.33, 5,683 cases).
- **F3:** The reversal exists only when the coin's recent volatility is raised against its longer baseline (168-hour volatility over 720-hour volatility). On the 24-hour grid the slope of excess return on the negated volatility-scaled 24-hour move is:
- **F4:** Inside that volatility measure the effect is graded. The 24-hour slope t rises across vol-ratio quintiles: 0.04, -1.44, -1.49, 3.15 (ratio 1.07), 6.45 (ratio 1.38). The hot-state slope also holds at 12 hours (t 5.37) and at 48 hours (t 4.76, slope 0.0075 against 0.0060 at 24 hours).
- **F5:** The book's gain before costs follows the same split. It is +0.0015 a day in the hot state, against -0.0013 in the calm state and +0.00006 in the mid state, but fees run 0.0025 to 0.0030 a day in every state. So even the hot state alone does not cover costs at the current turnover.
- **F6:** The reversal is lopsided toward falls. The bottom decile of the 24-hour scaled move (-1.73 usual moves) is followed by +0.56% excess over 24 hours, while the top decile (+1.89) is followed by only -0.20%. The re-standardised forecast also tracks the raw move more weakly (slope t 3.02 against 3.84).

## Ideas
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal.d1_reversal-in-volatility-spikes` (from F1, F3, F4, F5): Over the next 24 hours, a coin moves against its 24-hour return, and the larger that return relative to the coin's usual volatility, the larger the reversal, only while the coin's past-week volatility is raised above its past-month volatility, and the more raised it is, the larger the reversal.
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal.d2_slow-rebound-after-volatile-drops` (from F2, F3, F4, F6): Over the next 2 days, a coin rises after a fall in its 24-hour return, and the larger that fall relative to the coin's usual volatility, and the more its past-week volatility exceeds its past-month volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
