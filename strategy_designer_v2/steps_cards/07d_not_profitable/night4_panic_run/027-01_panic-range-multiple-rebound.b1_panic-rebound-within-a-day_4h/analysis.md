---
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
idea tested: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3918 USD
---
## Findings
- **F1:** The book did not beat holding the coins. Its Sharpe was 0.541 against holding's 0.554, and its mean daily return was 0.000546 against holding's 0.001179. Its Calmar was 0.28, because its deepest fall of -49.2 % over 27 days in w16 is set against a yearly return of only 13.7 %.
- **F2:** Fees ate 7.19 of the book's 17.14 summed bar gains, which is 42 %. In the forecast 5–20 bucket alone, fees were 3.56 against a gain of 9.95. This matches the size check: the unusual move per case, +0.19 %, is only 1.0 times the 0.19 % cost of a trade.
- **F3:** The effect sits only in the strongest panics.
- **F4:** Among strong cases (forecast ≥ 1), the return was U-shaped in the coin's 7-day return before the panic.
- **F5:** The book's deepest falls were carried by its strong panic signals.
- **F6:** Positions held after the signal had faded added no gain but still carried market exposure.

## Ideas
- `027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day.d1_panic-after-extreme-week` (from F4, F5, F1): When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 24 hours, and the larger that range multiple, the higher the return. This holds only while the coin's 7-day return before the stretch lies far from zero, and the return grows with how far that 7-day return lies from zero.
- `027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day.d2_deepest-falls-carry-rebound` (from F3, F2, F6): When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 24 hours, and the larger that range multiple, the higher the return. That return rises faster than in proportion to the depth of the 24-hour fall measured in the coin's usual 24-hour moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
