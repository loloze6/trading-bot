---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3977 USD
---
## Findings
- **F1:** The fall is graded by the cluster and the book loses on the weak end of it. On active bars, split into quintiles of the raw cluster reading, the unusual long-side 5-day move runs +0.81 % (351 cases, t 1.12), -0.33 %, -0.38 %, -0.78 %, -0.89 % (351 cases, t -2.13). The book was still short in the lowest quintile, at a mean allocation of -0.22, so it bet on a fall where the coin rose more than usual.
- **F2:** Only the largest clusters cover a trade, and only narrowly. The top quintile's unusual fall of 0.89 % per case is about 0.08 of the coin's usual 5-day move (10.6 %) and 4.7 times the 0.19 % cost. Against the coins' rising drift of about +0.59 % per 5 days, its total short move is only about +0.30 %, 1.6 times the cost. Over all 1355 cases the total move is -0.40 %, -2.1 times the cost.
- **F3:** The large-cluster fall is concentrated in falling years. In the top quintile the unusual long-side move was -6.2 % in 2018 (21 cases), -2.5 % in 2019 (52), -1.7 % in 2021 (25) and -1.8 % in 2022 (44). It was +1.5 % in 2020, +0.2 % in 2023 (79), -0.1 % in 2024 (61) and +0.4 % in 2025 (43). The book's mean daily return was positive in 2018 (+0.09 %) and 2022 (+0.12 %), when the coins fell (-0.35 % and -0.18 % a day). It was negative in 2020, 2021, 2023 and 2024, when they rose (+0.15 % to +0.42 % a day).
- **F4:** Being below the 50-day average carries little effect on its own. The unusual 5-day move is -0.32 % below the average (1781 cases) against +0.35 % above it (1638). It is not graded by depth either: bars more than 20 % below the average show +0.07 % (202 cases).
- **F5:** A large cluster is followed by a fall whatever the 20-day move. Large clusters show -0.87 % after a deep 20-day fall (188 cases, t -1.27) and -0.82 % after a shallow one (513 cases, t -2.34). Small clusters after a shallow 20-day move show +0.53 % (508 cases, t 1.04).
- **F6:** Most trades lose and a few large wins carry the mean. The book made 3269 short trades, with a median holding of 5 days and a mean of 11.3. The mean gross gain per trade was +0.23 % and the mean net gain +0.13 % after about 0.24 % commission, but the median trade lost 1.55 % net.
- **F7:** Step 5's supporting check had no cases in its larger half. 41 % of active forecasts sit at the cap (|forecast| ≥ 19, median -7.2). This leaves the graded half-split of the verdict empty, while the raw reading itself is graded (F1).
- **F8:** The effect differs by coin. Across the top two cluster quintiles the unusual long-side move is -2.24 % on ZEC, -0.56 % to -0.85 % on BTC, ETH, LTC and XRP, and +0.03 % on XMR (110 to 131 cases each).

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend.d1_broken-lows-in-falling-quarter` (from F1, F2, F3, F4, F5): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie within a few percent above the close, the larger the fall, only while the close is below its 50-day average price and the coin's 90-day return is negative, the fall growing the more negative that 90-day return.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend.d2_crowded-broken-lows-only` (from F1, F2, F6, F7): When a coin's daily close sits below its 50-day average price, it tends to fall over the next 5 days by more the more of its past-90-day turning-up lows are clustered within a few percent above the close. The fall grows with the count of such lows faster than in proportion, so that a single distant low above the close is followed by a rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
