---
line: 7.c no effect
backtest: 089-01_calm-decline-up-volume-share_1d
idea tested: 089-01_calm-decline-up-volume-share
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5035 USD
---
## Findings
- **F1:** Inside the falling calm profile, the up-day share of 20-day volume does not predict the coin's drift-adjusted return. On non-overlapping grids its slope t is 0.67 at 5 days (121 cases), -0.72 at 10 days (57) and -1.35 at 20 days (28). Its top quartile at 5 days averages +0.16 % against -3.27 % for the bottom quartile, but the middle quartiles do not line up (-0.56 %, -2.59 %). The step-5 slope on the forecast is t -1.14, and the cases' unusual move is -0.66 % (t -1.31, 306 days).
- **F2:** Measured per day instead of as a share, the volume lean points the other way. The log ratio of mean up-day volume to mean down-day volume over 20 days has an in-profile slope t of -2.05 at 3 days (216 cases), and every 3-day grid offset is between -1.67 and -2.05. At 5 days it is t -1.41 (121 cases). By ratio quartile at 3 days, the heaviest down-day volume averages +1.16 % and the heaviest up-day volume -1.86 % (54 cases each, monotone).
- **F3:** The opposite effect is carried by ETH and ZEC. At 3 days ETH has t -2.61 (75 cases) and ZEC t -2.85 (56); at 5 days ETH has t -1.83 and ZEC t -2.06. BCH (t +0.66) and XMR (t +0.73) are flat. By year, the clearest is 2018 (t -2.17, 49 cases), and 2019 and 2021 are near zero.
- **F4:** The share's positive link sits outside the brief's profile, against the brief's own test. Out of profile the share slope is t 1.58 at 5 days (572 cases) and t 2.20 at 10 days (286). In profile it is 0.67 and -0.72.
- **F5:** What little the share carries in profile comes from the count of up days, not from volume. The 20-day up-day count has slope t 2.47 at 3 days (216 cases) and 1.81 at 5 days (121), while the per-day volume ratio is negative (F2).
- **F6:** The falling calm profile itself kept falling. The drift-adjusted in-profile return is -0.29 % at 3 days (255 cases), -0.83 % at 5 days (t -1.0, 146) and -2.67 % at 10 days (t -1.5, 70). Long cases therefore start against a headwind: their total move is -0.02 % per case against a 0.31 % trade cost.

## Ideas
- `089-01.c1_calm-decline-down-volume-exhaustion` (from F2, F3, F1): In a falling, calm market, the heavier a coin's average down-day volume has been against its average up-day volume over the last 20 days, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
