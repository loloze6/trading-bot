---
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.2779 USD
---
## Findings
- **F1:** The book's deepest fall, −26.7 % against a yearly return of +10.2 % (Calmar 0.30), ran over 412 days from w3 to w7, while the coins' summed daily returns fell −69.8 %. The book lost −22.1 % in that stretch: −10.5 % in w4, −7.3 % in w5 and −4.3 % in w7. In w4 to w7 every one of its Monday, Tuesday and Wednesday holdings lost (−8.1 %, −12.0 %, −7.0 % summed) as the coins kept falling on those weekdays (−42 %, −25 %, −31 %). In every window from w8 to w24 the book gained (+1.9 % to +5.8 % each, except w13 at −1.5 %).
- **F2:** Split by the coin's 30-day return before the Sunday, the quarter of the 2418 weekend-fall cases with the lowest one (below −12.5 %) rebounded only +0.35 % over 3 days (t 0.66, 604 cases), with the largest loss per position (−28 %). The other three quarters rebounded +1.22 %, +1.37 % and +2.16 % (t 2.86, 3.81, 4.71), with losses per position no worse than −8.4 %.
- **F3:** The condition alone is not the effect. On non-overlapping 3-day stretches with no weekend fall, a coin whose 30-day return was above −12.5 % rose +0.49 % (15437 stretches), against +1.58 % (t 9.6) when a weekend fall came on top of the same condition. This fits the brief's theory: a weekend fall that is only the cost of thin liquidity fades on Monday, while a fall inside a 30-day slide is part of a move carried by information, which keeps going.
- **F4:** Split by the coin's 30-day daily volatility against its 180-day volatility, the quarter of cases with the most excited volatility rebounded only +0.42 % (t 0.89), with the widest spread of position gains (0.048 against 0.022 to 0.027). The calmer three quarters rebounded +1.18 % to +1.81 % (t 3.1 to 4.9).
- **F5:** Rebuilt from the record, with the Monday-to-Wednesday holdings removed after Sundays whose prior 30-day return was below −12.5 %, the book's Calmar is 0.83 (deepest fall −13.7 %, yearly +11.4 %, Sharpe 0.88). Leaving out the excited-volatility cases instead gives a Calmar of 0.79. Leaving out both gives a Calmar of 0.90 (deepest fall −9.0 %, Sharpe 1.02).
- **F6:** Coins above their 50-day mean on the Sunday rebounded +1.96 % (t 5.16, 1013 cases), against +0.58 % (t 1.38, 1291 cases) below it.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound.d1_weekend-fall-outside-slides` (from F1, F2, F3, F5, F6): A coin's Saturday-to-Sunday close-to-close fall, measured in percent of its price, is followed by a rise over the next 3 days (Monday to Wednesday), and the deeper the percent fall, the larger that rise, while the coin's 30-day return before the weekend has not been a deep fall; the higher that 30-day return, the larger the rebound.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound.d2_weekend-fall-in-calm-markets` (from F1, F4, F5): A coin's Saturday-to-Sunday close-to-close fall, measured in percent of its price, is followed by a rise over the next 3 days (Monday to Wednesday), and the deeper the percent fall, the larger that rise, while the coin's last 30 days have been calm against its last 180 days; the calmer they were, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
