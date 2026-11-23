---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4728 USD
---
## Findings
- **F1:** In falling coins (20-day return below 0), the 5-day return scaled by 60-day daily volatility predicts the next 5 days' excess return downward and graded: Spearman rho −0.105 (p 0.0004, 1121 non-overlapping cases). The lowest octile is followed by −0.83 % and the highest octile by −2.33 % (t −2.56). The two octiles below it are followed by −1.33 % and −0.85 %. In rising coins the same relation is absent (rho 0.009, p 0.75, 1223 cases).
- **F2:** Inside the book's own active shorts, the gain over the coin's drift is carried by coins that had just risen. Shorts whose 5-day return was in the top quartile (+2 % to +27 %) earned +2.98 % per 5 days (t 4.64, 243 cases). The other three quartiles earned only +0.39 % to +0.67 % (t ≤ 1.29).
- **F3:** Shorting a falling coin after a 5-day rise beat the drift in 7 of 8 years and in 14 of 15 coins. The year means were +1.7 % in 2025 (t 2.32, 128 cases) and +2.3 % in 2024 (t 2.26, 86 cases). The only negative year was 2021 (−1.9 %, t −1.39). Among coins, ZEC was +3.0 % (t 2.02) and the only negative coin was XMR at −0.6 %. With a sample this small per coin, the breadth is suggestive, not proof.
- **F4:** The tested forecast is graded the wrong way, which matches its failed supporting check (−0.40 %):
- **F5:** The book's daily return moves against its coins' mean daily return, correlation −0.55. On its worst 2 % of days the coins rose 7.7 %, and on its best 2 % they fell 8.2 %. The book is a short coin exposure: Sharpe −0.05 against holding's +0.53, over 7.94 years.
- **F6:** Bars with a wide high-low range were followed by a higher 5-day excess return. The top quintile (range ≥ 9.1 % of close) gave +1.17 % (t 2.60, 947 cases), on down days +1.43 % (t 2.62) and on up days +0.96 % (t 1.20). Across years it was mixed: positive in 5 of 8, significant only in 2022 and 2024. Given the number of angles examined, this is not a finding to build on.
- **F7:** Weekday effects in daily excess returns reach large t on the pooled sample: Saturday +0.30 % (t 4.47), Tuesday −0.26 % (t −3.28), Thursday −0.26 % (t −3.02). They are unstable across years, though. Sunday ranges from −0.52 % (t −2.79) in 2022 to +0.54 % (t 1.96) in 2021, and Tuesday is significant only in 2024 (t −3.75). I treat them as not distinguishable from chance.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.g1_bounces-fade-in-downtrends` (from F1, F2, F3, F4, F5): When a coin's 20-day return is negative, the larger its 5-day rise relative to its usual daily volatility over the past 60 days, the larger its fall over the next 5 days compared with its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
