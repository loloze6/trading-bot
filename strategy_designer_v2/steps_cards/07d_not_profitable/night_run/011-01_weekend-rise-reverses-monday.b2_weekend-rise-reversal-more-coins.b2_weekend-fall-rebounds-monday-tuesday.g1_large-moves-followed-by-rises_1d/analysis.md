---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5856 USD
---
## Findings
- **F1:** The book's Calmar is 0.38 (yearly 15.4 %, deepest fall -40.3 %), and that fall runs 294 days from w1 to w3, while holding the coins fell -69.6 % over the same days. In w1–w3 the long positions taken after up days in down and up trends summed to -0.55 and -0.37, against +1.15 after down days in down trends.
- **F2:** The book's Sharpe of 0.6073 only ties holding's 0.6075. Its mean per-bar gain of 0.000957 is about half the market's own rise (0.000445) and half timing (0.000508), at a mean allocation of 0.30.
- **F3:** The gain sits in uptrends. Ranked by the coin's price against its 50-day average, the mean per-bar gain is 0.00188 in the top tercile, against 0.00051 in the middle and 0.00030 in the bottom, and the top tercile carries 17.4 of the 24.9 summed gain.
- **F4:** A large up day (|z| > 1) is followed by a negative excess 2-day return when the coin is in its down tercile against the 50-day average (-0.00797, t -2.27, n 426), and by a positive one in its up tercile (+0.01060, t 3.64, n 1060). By the 30-day return quintile, the excess after large up days grades monotonically from -0.00926 (t -1.78) in the lowest quintile to +0.01318 (t 3.14) in the highest.
- **F5:** A large down day is followed by a rise in every trend state: +0.00539 (t 1.90) in the down tercile and +0.00749 (t 1.77) in the up tercile. It is strongest in the lowest 30-day return quintile (+0.01031, t 2.86, n 461), so the rebound after falls does not depend on trend the way the follow-through after rises does.
- **F6:** In a pooled regression the forecast-times-trend-sign term is as strong as the forecast itself (beta 0.00032, t 4.95, against the forecast's t 4.90).
- **F7:** Re-running the book's gains without fees and setting the position to zero after up days below the 50-day average lifts the Sharpe from 0.93 to 1.22. It also lifts the Calmar from 0.78 to 1.50 (yearly 36.7 %, deepest fall -24.4 % against -35.4 %).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises.d1_large-moves-rises-need-trend` (from F1, F3, F4, F5, F6, F7): The larger a coin's 1-day move relative to its own 60-day volatility, in either direction, the more that coin rises over the next 2 days. The exception is after an up day: there the rise that follows is larger the higher the coin's 30-day return, and becomes a fall the more negative its 30-day return is.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises.d2_downtrend-rallies-fade-quickly` (from F1, F4): The larger a coin's 1-day rise relative to its own 60-day volatility, the more that coin falls over the next 2 days, and the more negative its 30-day return, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
