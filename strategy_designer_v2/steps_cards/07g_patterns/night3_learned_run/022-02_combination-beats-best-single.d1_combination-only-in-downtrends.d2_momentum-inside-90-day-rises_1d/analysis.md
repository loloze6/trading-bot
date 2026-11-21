---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3786 USD
---
## Findings
- **F1:** Inside 90-day falls (the `unknown` regime, flat in this book), the coin's 20-day volatility is graded against its next 5-day return net of drift: slope +0.063 of a usual move per standard deviation of volatility, t 2.54, on 1304 non-overlapping cases. By quintile of each coin's volatility the 5-day unusual move rises steadily: -1.00 %, -0.44 %, -0.35 %, +0.09 %, +0.19 %. That is a 1.2 % spread against a 0.19 % round trip. The slope is positive on all 6 coins (0.02 to 0.11, none with t above 1.6 alone) but carried by windows w13-24 (t 2.84, n 586); on w1-12 it is -0.47. Given the more than 20 angles looked at, this sits at the edge of chance.
- **F2:** The book's gain comes from its longs inside 90-day rises: their bar gains sum to 13.98, against 1.67 for the shorts there. Per trade, longs net +9.90 % on average (2282 trades) and shorts -1.06 % (median -1.82 %, 1393 trades). Shorts lose on average on every one of the 6 coins (-0.17 % to -2.13 %).
- **F3:** Inside 90-day rises, nearness to the 20-day high predicts the next 5 days (slope +0.071, t 2.64, n 1465), with quintiles rising from -0.37 % to +1.34 %. It correlates 0.47 with the forecast, and once the forecast is in the regression it falls to t 1.36 while the forecast keeps t 2.66. It is mostly the tested momentum seen another way, not a separate effect.
- **F4:** Inside 90-day falls, every momentum measure turns to a weak reversal: 1-day return slope -0.047 (t -2.01), 20-day return -0.039 (t -1.65). The 20-day reversal holds only on w1-12 (t -2.97, n 718) and not on w13-24 (t +0.46). It does not carry forward.
- **F5:** Next-day returns by weekday reach t of -2.7 to +3.8 (for example +0.30 % on Saturdays, n 2479). These counts pool 6 coins that move together, and the pattern is not graded, so it is not used as a finding for an idea.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises.g1_volatility-inside-90-day-falls` (from F1, F4): While a coin's 90-day return is negative, the higher its 20-day volatility, the higher its return over the next 5 days; quiet stretches inside a fall keep falling and turbulent ones do not.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
