---
line: 7.g patterns
backtest: 032-02.g1.e2.e1_new-closing-high-continuation_1d
idea tested: 032-02.g1.e2.e1_new-closing-high-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5543 USD
---
## Findings
- **F1:** A day whose fall is large against the coin's typical daily move over the past 20 days is followed by a next-day return above the coin's average, and the larger the fall, the larger the rebound. Falls of 2 to 3 typical moves are followed by +1.38 % next day (t 2.49, 147 cases on 76 days), and falls of 1 to 1.5 typical moves by +0.84 % (t 2.03, 436 cases on 217 days). Without day clustering, falls of at least 2 typical moves are followed by +1.64 % (t 3.90, 220 cases), while days between -1 and +1 typical moves are followed by +0.02 % (t 0.27, 5283 cases). On days down at least 1 typical move, the fall's size is correlated with the next day's excess at -0.103.
- **F2:** The next-day rebound after falls of at least 1 typical move points the same way in every subgroup: in all 4 years (+0.68 %, +0.06 %, +1.35 %, +1.88 %… exactly +0.0068, +0.0006, +0.0135, +0.0143), in all 6 coins (+0.32 % for BTC to +1.21 % for XMR, XMR t 2.89, ZEC t 2.03), and in both 28-day trend states (+0.85 % t 1.61 when the 28-day return is negative, +0.87 % t 1.95 when it is positive).
- **F3:** The rebound is a one-day effect. Over the next 3 days, on a non-overlapping grid, falls of 2 to 3 typical moves are followed by only +1.35 % (t 0.93, 51 cases) and falls of 1 to 1.5 typical moves by -0.30 % (t -0.24). Most of the move is gone after the first day.
- **F4:** Small up days (0 to 0.5 typical moves) are followed by a next-day excess of -0.43 % (t -2.29, 1671 cases on 719 days). Larger up days show no follow-through: +0.19 % (t 0.63) after 1 to 1.5 typical moves and -0.06 % (t -0.15) after more than 2. On a one-day horizon there is no symmetric momentum after up days.
- **F5:** The tested book was in a position on 71 % of the days that fell at least 1 typical move, so it holds this rebound without seeking it. Its result depends on rare days: the top 5 % of book days sum to 4.26 and the bottom 5 % to -3.91, against a total of 1.91. The book lost in 2018 (mean daily -0.11 %, t -1.27) and earned mostly in 2020 (+0.40 %, t 2.82).
- **F6:** The brief's calm-decline continuation does not show here. On grid cases with a negative 28-day return, the calmest volatility tercile is followed by +2.40 % excess over 10 days (t 0.83, 106 cases), the opposite of a further fall. Within that tercile, the 28-day return is correlated with the excess at only +0.17, and the bars cannot tell this from chance.
- **F7:** Coin returns are higher on Fridays (+0.54 %, t 3.75) and Saturdays (+0.58 %, t 4.24), and the book's are too (t 2.46 and 2.89). Measured as excess and split by year, the effect is not stable: Saturday is negative in 3 of 4 years. I take it as no finding.

## Ideas
- `032-02.g1.e2.e1.g1_next-day-rebound-after-shock` (from F1, F2, F3): In a coin, the larger the day's fall measured against its typical daily move over the past 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
