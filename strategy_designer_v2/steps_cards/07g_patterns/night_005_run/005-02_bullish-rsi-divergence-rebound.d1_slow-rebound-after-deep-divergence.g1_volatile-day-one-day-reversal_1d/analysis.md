---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3389 USD
---
## Findings
- **F1:** The one-day give-back sits only in the top quarter of the 20-day/60-day volatility ratio: the slope of next-day excess return on the scaled move z is -0.00554 (t -4.34, n 983) there, against +0.00042 (t 0.34), +0.00069 (t 0.59) and -0.00074 (t -0.61) in quartiles 1 to 3 (about 980 bars each), and both coins agree in that top quartile (BTC t -2.61, n 544; ETH t -3.54, n 439).
- **F2:** In the top volatility-ratio quartile the give-back lasts beyond one day: on non-overlapping 3-day samples, the slope of the 3-day excess return on the day's z is -0.0133 (t -3.91, n 324), more than twice the one-day slope; on all high-volatility bars it is -0.0068 (t -2.57, n 573).
- **F3:** The give-back in volatile spells is mostly a rebound after down days: in the top volatility-ratio quartile, down days have a slope of -0.00936 (t -3.21, n 480) against -0.00139 (t -0.62, n 503) for up days, and days with z below -1 are followed by a mean next-day excess return of +1.64% (t 3.12, n 123), against -0.45% to +0.23% after such days in the other quartiles.
- **F4:** In the calmest quarter of the volatility ratio the sign turns: the day's z predicts continuation over the next 3 days (slope +0.0105, t 3.08, n 319, non-overlapping), and on low-volatility bars the slope is +0.0042 (t 2.14, n 998), positive for both coins (ETH t 2.12, BTC t 1.09).
- **F5:** The book's gain is all timing and no market: timing is 0.000687 per bar against a market part of -0.000017, while the book is flat on 43% of bars and earns a mean daily 0.000384 against the coins' 0.001275. Holding the coins beats it because it gives up their rise, not because the reversal is absent.
- **F6:** Weekday next-day returns (Wednesday -0.39%, t -2.39, n 830; the other days |t| ≤ 1.6) and the book's extreme days (worst 2%: same-day coin move -0.7%, half of them up days) show nothing that stands out after this many angles.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal` (from F1, F2): When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the higher the volatility ratio, the larger the move back.
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g2_volatile-down-day-rebound` (from F3, F1): When a coin's 20-day volatility is high relative to its 60-day average, a down day is followed by a rise over the next 1 day. The larger the day's fall relative to its 20-day volatility, the larger the rebound.
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g3_calm-spell-three-day-continuation` (from F4, F5): When a coin's 20-day volatility is low relative to its 60-day average, its return over the next 3 days follows the direction of the day just closed. The larger that day's return relative to its 20-day volatility, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
