---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3799 USD
---
## Findings
- **F1:** Large hourly falls rebound strongly while large hourly rises barely fade. Over the next 2 hours (non-overlapping, excess over the coin's drift), falls beyond -4 usual moves are followed by +35.3 bp (t 5.55, n 2304) and falls of -2.5 to -4 by +16.1 bp (t 5.59, n 5078). Rises of 2.5 to 4 and beyond 4 are followed by only -2.7 bp (t -0.93) and -5.4 bp (t -1.02). The tested short-the-rise idea sits on the weak side of this asymmetry.
- **F2:** The rebound after falls clears the cost of a trade, unlike the tested idea. Falls beyond -4 usual moves are followed by a total 2-hour move, drift included, of +36.5 bp, against a trade cost of 19 bp. For falls beyond -2.5 it is +23.3 bp. The tested idea's total move was +3 bp.
- **F3:** The rebound is largest on surging volume, the opposite of the brief's continuation. After falls beyond -2.5 usual moves, the 2-hour excess is +38.2 bp (t 6.77, n 2638) when volume is above 3 times its 30-day mean, against +9.1 bp (t 1.26) near average volume. Pooled over both directions, big moves on volume above 3 times average reverse by 24.7 bp over 2 hours (t -6.32, n 5074).
- **F4:** The rebound grows with the recent volatility regime. After falls beyond -2.5 usual moves, the 2-hour excess is +44.7 bp (t 6.79) in the top tercile of 24-hour versus 30-day volatility and +7.3 bp (t 2.33) in the bottom tercile. The reversal of big moves in both directions follows the same order: -16.2 bp (t -7.13) in the top volatility quartile against +6.4 bp (t 1.49) in the bottom.
- **F5:** The rebound after large falls holds across every coin and most years.
- **F6:** Larger multi-hour selloffs bring larger rebounds over the next 4 hours. A 6-hour fall beyond -6 usual 6-hour moves is followed by +122.7 bp (t 3.73, n 285), a fall of -4 to -6 by +24.1 bp (t 1.93), and -2.5 to -1 by +5.4 bp (t 2.61). The lowest quintile of 24-hour momentum is followed by +9.6 bp over 6 hours (t 3.40).
- **F7:** The book lost before costs on every coin, so its loss is not only the fee. It lost -0.1 % a day (Sharpe -3.74). Mean gross trade returns of the 2-hour trades run from -0.11 % (BTC) to -0.52 % (ZEC), while every coin rose on average (+6.7 to +15.5 bp a day).
- **F8:** The hours 20 and 21 UTC carry an hourly excess of +4.8 bp (t 5.98) and +3.7 bp (t 4.85). This is positive on all six coins (t 2.5 to 3.9) and in 7 of 8 years (2022: -2.8 bp). At about a fifth of the 19 bp trade cost, it is far too small to trade alone.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins.g1_high-volume-flush-rebounds` (from F1, F2, F3, F5): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume well above its 30-day average hourly volume, the price rebounds over the next two hours. The larger the fall and the larger the volume surge, the larger the rebound.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins.g2_turbulent-regime-drop-rebound` (from F1, F4, F5): When the coin's volatility over the past day is high relative to its past 30 days, an hourly fall far larger than its typical hourly move is followed by a rebound over the next two hours. The higher the recent volatility and the larger the fall, the larger the rebound.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins.g3_deep-six-hour-selloff-rebound` (from F6, F1): The further the coin's 6-hour return falls below its typical 6-hour move over the past 30 days, the more it rises over the next four hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
