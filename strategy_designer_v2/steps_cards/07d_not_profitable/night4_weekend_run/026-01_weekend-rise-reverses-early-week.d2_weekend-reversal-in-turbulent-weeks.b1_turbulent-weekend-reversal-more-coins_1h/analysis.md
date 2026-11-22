---
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6515 USD
---
## Findings
- **F1:** The book's short is not closed after Monday and Tuesday. Of 826,743 recorded bars, 70,135 carry a short outside the 48 hours after a Monday 00:00 bar, and none carry a long. Those out-of-window bars sum to a gain of -0.70, against +2.15 inside the window. Trades last a mean of 99 hours (median 48, maximum 2,833), and the leftover position most often sits on Wednesday (130 coin-windows).
- **F2:** Because of those overstays, the 1,586 trades average -1.22 % net (t -3.99, 28 % winners). This is against a mean short move of +0.90 % over the idea's own 48 hours on the 985 Monday cases (t 3.08).
- **F3:** The fall does not grow with the weekend gain; it shrinks as the forecast grows:
- **F4:** The fall grows with the coin's 30-day hourly volatility. By volatility quintile, the 48-hour short move is -0.81 % (t -0.99), +0.80 %, +0.90 %, +1.09 % and +1.79 % (t 2.19), about 155 cases each.
- **F5:** The effect rests on a few periods, which is why the leave-one-window-out Sharpe fails (-0.188):
- **F6:** Most of the fall comes on Tuesday. The short move is +0.18 % over the first 24 hours and +0.72 % over the second 24 hours (985 cases).
- **F7:** The fall is largest after a 30-day decline. It is +1.68 % (t 2.54) when the 30-day return is in its lowest quintile (-60 % to -21 %) and +1.31 % (t 2.27) in the next. It is -0.97 % (t -1.66) when the 30-day return is near flat (-4 % to +17 %).

## Ideas
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins.d1_turbulence-graded-weekend-rise-reversal` (from F4, F3, F1, F2): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months; the higher the coin's 30-day hourly volatility at Monday 00:00, the larger the fall.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins.d2_tuesday-fade-after-weekend-rise` (from F6, F4, F1): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), mostly over Tuesday, only while the coin's 30-day hourly volatility is high against its own last 6 months; the higher that volatility, the larger Tuesday's fall.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins.d3_weekend-rally-fades-in-downtrends` (from F7, F5, F4): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months and its 30-day return is negative; the deeper its 30-day fall, the larger the fall after the weekend rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
