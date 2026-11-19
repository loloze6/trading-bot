---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3631 USD
---
## Findings
- **F1:** The tested 20:00 position is held for one hour, not the 24 hours the idea measures, so the book cannot carry the rebound: its 7238 trades last 61 minutes on average, gross -0.095 % and net -0.195 % per trade (about 0.1 % fees each), and the 20:00→21:00 hour itself averages only +0.000051 (t 0.63), giving a book mean daily return of -0.000408 and Sharpe -2.24 over 2898 days.
- **F2:** The 24-hour reversal sits almost entirely in high-volatility days. On the non-overlapping daily grid, the slope of the next-24h excess return on the past-24h return has t -8.91 in the top quintile of 24h summed absolute hourly moves (n 3422), against t between -0.50 and +1.24 in the other four quintiles. It is negative in all six coins on those days (t -2.15 to -4.92).
- **F3:** Inside that top-volatility quintile the response is graded and two-sided. The deepest-fall quintile (mean past return -11.8 %) gains a next-24h excess of +2.05 % (t 6.15, n 685). The quintiles above it fall steadily to -0.72 % (t -2.32, n 685) after the largest rises (+13.0 %).
- **F4:** Contrary to the brief, moves made with evenly spread volume reverse more than volume-burst moves. The reversal slope is -0.135 (t -9.91) in the least-concentrated volume tercile, -0.075 (t -5.56) in the middle one and -0.032 (t -2.56) in the most-concentrated one. In the pooled regression, past × max-hour volume share is +0.375 (t 4.63). The share of the move made in a single hour changes little (slopes -0.071 / -0.101 / -0.078).
- **F5:** Hourly returns closing at 22:00 and 23:00 UTC average +0.00055 (t 6.87) and +0.00044 (t 5.76), against about +0.00002 for the other hours. This holds in all six coins (Welch t 2.73 to 4.22) and in 7 of 8 years (2022 is the exception at -0.00022).
- **F6:** Saturday hourly returns average +0.000269 (t 7.22), the largest weekday mean; the next is Wednesday at +0.000149 (t 3.22).

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.g1_high-volatility-daily-reversal` (from F2, F3, F1): On days when a coin's hourly moves have been large, the more it has fallen over the past 24 hours, the more it rises over the next 24 hours, and the more it has risen, the more it falls.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.g2_even-volume-moves-reverse-more` (from F4, F2): The more evenly a coin's volume was spread across the hours of its past-24-hour move, the larger the share of that move it gives back over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
