---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On days a coin closes lower, the further that day's high-low range exceeds the coin's average range over the past 30 days, the higher the coin's return over the next 3 days above its usual drift, the move growing fastest among the widest falling days and taken only on the long side.
Consequence: A trader would buy only after falling days far wider than the coin's 30-day norm, sized by how wide, hold for 3 days, and never short narrow falling days.
Why:
- F1: The book's gain comes only from its widest falling days: held bars with forecast above 4 earned 0.00206 per bar (sum 1.63 of the book's 2.74 total), while the 8,891 held bars with forecast near 0 and the 5,208 bars with negative forecast earned together −0.0000 sum ≈ +0.05. This matches the idea's own decile reading on falling days: the 3-day excess return is +3.07 % in the top range-ratio decile (mean ratio 2.68) and +1.63 % in the ninth (1.54), and between −1.10 % and +0.34 % in deciles 0 to 7 (225 cases each).
- F2: The short side, which the graded adaptation takes on narrow falling days, loses. Short bars summed −0.135 against +2.87 for long bars, and short trades averaged −1.69 % net over 2,528 trades against +2.00 % net over 2,146 long trades. So the book sits in a position on 82 % of coin-days to earn its mean of 0.000145 per day in a position, below the 0.0005 rule.
- F3: Kept to its strong case, the book passes both failed measures (rebuilt from bar gains, before fees). Long-only on bars with forecast above 2 is in a position on 7.9 % of coin-bars, makes 0.00162 per bar in a position (more than 3 times the 0.0005 rule) and has a Calmar of 0.93 (yearly +4.7 %, deepest fall −5.0 %, Sharpe 1.15). The full book has a deepest fall of −12.2 % and a Calmar of 0.34. All longs together reach Calmar 0.68 and Sharpe 0.89.
- F4: The effect lives in the first 3 days. For top-quintile wide falling days, the strength is 0.168 at 1 day (t 5.2, n 1,447) and 0.279 at 3 days (mean excess +2.35 %, t 5.1, n 449). It is 0.075 at 5 days (t 1.3), −0.030 at 7 days and 0.065 at 10 days. The 3-day hold is right, and a longer holding would not help.
- F6: On falling days, a deep fall helps only when the range is wide. In the deepest quarter of 1-day falls, wide-range days gave +1.27 % 3-day excess (450 cases) and narrow-range days −1.27 % (226 cases). The width of the day carries the signal, and the size of the fall does not.
