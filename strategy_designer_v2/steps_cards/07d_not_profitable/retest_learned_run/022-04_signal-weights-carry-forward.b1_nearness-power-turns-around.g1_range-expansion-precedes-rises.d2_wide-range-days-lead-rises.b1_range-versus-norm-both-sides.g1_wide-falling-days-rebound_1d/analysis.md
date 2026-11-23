---
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3841 USD
---
## Findings
- **F1:** The book's gain comes only from its widest falling days: held bars with forecast above 4 earned 0.00206 per bar (sum 1.63 of the book's 2.74 total), while the 8,891 held bars with forecast near 0 and the 5,208 bars with negative forecast earned together −0.0000 sum ≈ +0.05. This matches the idea's own decile reading on falling days: the 3-day excess return is +3.07 % in the top range-ratio decile (mean ratio 2.68) and +1.63 % in the ninth (1.54), and between −1.10 % and +0.34 % in deciles 0 to 7 (225 cases each).
- **F2:** The short side, which the graded adaptation takes on narrow falling days, loses. Short bars summed −0.135 against +2.87 for long bars, and short trades averaged −1.69 % net over 2,528 trades against +2.00 % net over 2,146 long trades. So the book sits in a position on 82 % of coin-days to earn its mean of 0.000145 per day in a position, below the 0.0005 rule.
- **F3:** Kept to its strong case, the book passes both failed measures (rebuilt from bar gains, before fees). Long-only on bars with forecast above 2 is in a position on 7.9 % of coin-bars, makes 0.00162 per bar in a position (more than 3 times the 0.0005 rule) and has a Calmar of 0.93 (yearly +4.7 %, deepest fall −5.0 %, Sharpe 1.15). The full book has a deepest fall of −12.2 % and a Calmar of 0.34. All longs together reach Calmar 0.68 and Sharpe 0.89.
- **F4:** The effect lives in the first 3 days. For top-quintile wide falling days, the strength is 0.168 at 1 day (t 5.2, n 1,447) and 0.279 at 3 days (mean excess +2.35 %, t 5.1, n 449). It is 0.075 at 5 days (t 1.3), −0.030 at 7 days and 0.065 at 10 days. The 3-day hold is right, and a longer holding would not help.
- **F5:** The rebound after a wide falling day is larger when the coin's 30-day return is positive: +3.09 % excess over 3 days (191 cases) against +1.80 % when it is negative (258 cases). The 30-day trend alone is worth only +0.25 % (up, 2,187 cases) against −0.15 % (down, 3,536 cases). So the trend condition is not an effect of its own; it strengthens the idea's overreaction-in-a-trend theory. The long side's losing years were the falling years, 2018 (−0.52) and 2022 (−0.29).
- **F6:** On falling days, a deep fall helps only when the range is wide. In the deepest quarter of 1-day falls, wide-range days gave +1.27 % 3-day excess (450 cases) and narrow-range days −1.27 % (226 cases). The width of the day carries the signal, and the size of the fall does not.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only` (from F1, F2, F3, F4, F6): On days a coin closes lower, the further that day's high-low range exceeds the coin's average range over the past 30 days, the higher the coin's return over the next 3 days above its usual drift, the move growing fastest among the widest falling days and taken only on the long side.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends` (from F5, F1, F4): On days a coin closes lower, the further that day's high-low range exceeds the coin's average range over the past 30 days, the higher the coin's return over the next 3 days above its usual drift, more so while the coin's 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
