---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3601 USD
---
## Findings
- **F1:** The tested result is near zero because the combined score and the best single score are almost the same bet. Their scaled values correlate at 0.83 over 1,704 trending cases, and their fits with the excess 5-day return are about equal: mean d 0.00048 (t 0.28), combined -0.0055 (t -1.79), best -0.0060 (t -2.14). Neither score beats the other because both fail.
- **F2:** In the 90-day rise, both learned scores point the wrong way, and the book followed them. Betting the sign of the combined score earned -0.80 % of excess 5-day return per case (t -2.79, 1,704 cases). The idea's measured size is -0.43 % unusual and -0.51 % total per case, against a 0.19 % round trip, and the book's Sharpe was -0.98.
- **F3:** The 28-day return on its own predicts the next 5 days with the usual sign inside the 90-day rise. Its correlation with the excess 5-day return is +0.112 (t 4.03, 1,272 cases). The cases rank from -2.1 % excess in its lowest fifth to +1.4 % and +1.0 % in its top two fifths, a spread of about 3 %, about 16 times the 0.19 % cost of a trade.
- **F4:** Outside the 90-day rise, the same signals carry the opposite sign: 28-day return correlation -0.084 (t -2.89, 1,178 cases), closeness to the high -0.078 (t -2.82). The 365-day correlation weights learn from a mix of both regimes, so they carry the reversal sign into uptrends. This is why the learned combination anti-predicts where the idea placed it.
- **F5:** Closeness to the 90-day high also predicts with its usual sign inside the rise. Its correlation is +0.080 (t 3.00, 1,417 cases), with excess returns of -1.24 % in its lowest fifth against +1.0 to +1.3 % in its top three fifths. The reversed 1-day return and the negated volatility add little (t -2.08 and +0.65).
- **F6:** The combined-minus-best difference shows in no consistent part of the data. By 90-day-return fifth, d runs -0.0096 (t -3.35), -0.0004, +0.0076 (t 2.57), -0.0040, +0.0088 (t 1.65). By coin and by year it is mixed and every t is below 1.5 in size. No condition or side makes the tested comparison clear.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.b1_momentum-inside-90-day-rises` (from F2, F3, F4): While a coin's 90-day return is positive, the higher its 28-day return, the higher its return over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.b2_nearness-to-high-in-uptrends` (from F4, F5): While a coin's 90-day return is positive, the closer its close is to its 90-day closing high, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
