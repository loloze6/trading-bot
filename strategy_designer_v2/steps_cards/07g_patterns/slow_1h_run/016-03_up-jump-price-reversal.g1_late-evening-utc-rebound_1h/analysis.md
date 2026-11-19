---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3833 USD
---
## Findings
- **F1:** The book loses because of fees, not because the forecast is wrong: the position's gain averages 0.116 bps per bar against 0.225 bps per bar of fees. The fee hits 2.39 bps on the 19:00 bar and 2.38 bps on the 21:00 bar, and each of the roughly 1,800–1,900 two-hour trades per coin nets −0.09 % to +0.05 % after costs, with four of six coins negative.
- **F2:** Coins rise at 20:00–22:00 UTC whatever came before. The 20:00 and 21:00 hourly bars average +5.45 bps (t 6.75, n 17,403) and +4.36 bps (t 5.66, n 17,417). The 2-hour return from the 20:00 close is +9.13 bps (t 7.38, n 12,600), the highest of all 24 start hours, positive in all six coins and in six of eight years.
- **F3:** The 24-hour reversal behind the idea holds over a full day, not only 2 hours. On a non-overlapping 24-bar grid, the slope of the next 24-hour return on the past 24-hour return is negative in every coin (−0.064 to −0.129, t −3.4 to −6.9, about 2,800 cases each) and in seven of eight years. The deepest-fall fifth gains +58.5 bps over the next 24 hours (t 5.69, n 3,423), while the 72-hour version is not significant (slope +0.016, t 1.16, n 5,539).
- **F4:** The 24-hour reversal is strongest when recent volatility is high against the week's. In the top fifth of 24-hour versus 168-hour volatility, the slope is −0.107 (t −8.47, n 3,249) against −0.065 (t −2.41) in the bottom fifth, and that top fifth also gains +34.4 bps over the next 24 hours on average (t 3.40).
- **F5:** How the 24-hour move was built changes nothing, which goes against the brief's grind-versus-jump split. Sorted into terciles by the largest hourly move's share of the day's total movement, the reversal slopes are −0.072, −0.097 and −0.081 (t −4.7, −7.0, −7.3, about 5,700 cases each).
- **F6:** The evening makes the reversal steeper. At the 20:00 close, the slope of the 2-hour return on the 24-hour return is −0.0189 (t −8.12, n 17,261), against −0.0062 (t −4.75, n 52,412) at the other odd hours. At 20:00 the deepest-fall fifth gains +21.3 bps over 2 hours (t 5.70), while the top fifth gains only +1.3 bps.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.g1_daily-fall-day-long-rebound` (from F3, F1, F5, F6): The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.g2_turbulent-fall-day-rebound` (from F4, F3): When a coin's 24-hour volatility is high relative to its 7-day volatility, the more it has fallen over its last 24 hours, the more it rises over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
