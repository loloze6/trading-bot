---
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
idea tested: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3057 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: the summed position gain before fees is 5.29 against 9.49 in fees; trades last a median 2 hours with a mean gross gain of 0.01–0.31% per trade against a mean commission of 0.27–0.54%, so four of six coins lose net (XRP −0.089%, XMR −0.061%, LTC −0.035% per trade).
- **F2:** The 2-hour edge is too small to pay a round trip: at the 20:00-stamped decision bars, the 2-hour return with a positive forecast is 0.12–0.14% by forecast bucket, against 0.064% with a zero forecast (n = 8,790), so the fall adds only about 0.06–0.08% per case.
- **F3:** The rebound sits in high-volatility states, where the sizing holds the least: among positive-forecast cases, the high-volatility tercile earns 0.23% over 2 hours and 0.38% over 24 hours, against 0.062% and 0.054% in the low-volatility tercile, while the mean position is 0.29 against 0.65 (n ≈ 2,688 each).
- **F4:** Measured as the raw 24-hour fall in the coin's own volatility, the rebound is graded and grows over a day: the deepest-fall quartile earns 0.22% over 2 hours and 0.43% over 24 hours, against 0.11% and −0.016% in the shallowest quartile (n ≈ 2,015 each).
- **F5:** The recorded forecast (standardised over 60 bars) is graded only at 2 hours and reverses after: its slope t is 2.78 at 2 hours, −3.71 at 6 hours and 0.59 at 24 hours, and its top bucket earns 0.076% over 24 hours against 0.44% for the 5–10 bucket.
- **F6:** One year breaks the effect: in 2022 the positive-forecast cases lose 0.096% over 2 hours and the book's position gain is −0.75, against positive gains in every other year.

## Ideas
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.d1_daily-drop-rebound-over-day` (from F1, F2, F4, F5): The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the next 24 hours that follow 21:00 UTC, not only over the two hours from 21:00 to 23:00 UTC.
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.d2_evening-rebound-in-turbulence` (from F1, F3): The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the two hours from 21:00 to 23:00 UTC that follow, and the more so the higher the coin's own volatility over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
