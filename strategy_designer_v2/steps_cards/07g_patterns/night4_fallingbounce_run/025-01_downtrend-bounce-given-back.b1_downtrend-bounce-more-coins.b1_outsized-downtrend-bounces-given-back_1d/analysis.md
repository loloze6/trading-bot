---
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4873 USD
---
## Findings
- **F1:** In coins whose 90-day return is positive, a large one-day rise is followed by a further rise over the next 5 days, not a fall. On days above 2 usual daily moves the winsorised unusual move is +5.06 % (t 3.96, 103 independent cases, 68 % of cases up). Between 1.5 and 2 moves it is +1.99 % (t 2.21, 163 cases). The link is graded across up days (Spearman 0.124, p < 0.0001, 1,636 cases).
- **F2:** The answer to a large up day depends on the 90-day trend. Up days above 2 moves end 5 days later lower in falling coins than in rising ones (Welch t −4.68). Up days above 1 move average +1.76 % in rising coins against −2.30 % in falling ones. That mean is positive in 84 % of the 19 coins when rising and in only 21 % when falling. In rising coins it is positive in 7 of 8 years, missing only 2025.
- **F3:** In falling coins, the 3-day return measured in usual moves predicts the next 5 days better than the one-day bounce the tested idea uses. The winsorised unusual move falls steadily across 3-day quintiles: +0.11 %, −0.44 %, −0.46 %, −1.02 %, then −1.70 % in the top quintile (t −3.69, 509 cases). The one-day measure is weaker: Spearman −0.065 (p 0.015, 1,414 cases), and its 1.5 to 3 move buckets have t of only −1.7.
- **F4:** In rising coins, the 30-day return measured in usual moves (its 20-day standard deviation times √30) predicts the next 5 days in the same direction. The winsorised unusual move climbs steadily from −2.51 % in the lowest quintile (t −3.01, 181 cases) to +1.25 % in the highest (t 3.07, 894 cases).
- **F5:** The book's losses come from squeezes while it is short.
- **F6:** The one-day result reported in step 5 does not come from the bounce size the forecast grades on. In the falling regime, the 5-day unusual move barely changes by forecast bucket: −1.31 % at forecast −10 or below, −1.00 % between −2 and −10, and −0.53 % when flat (t −1.96, −1.64 and −2.34). The falling regime as a whole drifts below the coins' normal drift.

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.g1_outsized-up-days-continue-uptrend` (from F1, F2): In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days, and the more usual daily moves the rise covers, the larger the further rise.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.g2_three-day-rallies-fade-downtrends` (from F3, F6): In a coin whose 90-day return is negative, the larger its 3-day return measured in units of its 20-day standard deviation of daily returns, the larger its fall over the next 5 days.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.g3_monthly-strength-persists-uptrend` (from F4, F2): In a coin whose 90-day return is positive, the higher its 30-day return measured in units of its 20-day standard deviation of daily returns scaled to 30 days, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
