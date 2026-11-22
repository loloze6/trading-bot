---
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3637 USD
---
## Findings
- **F1:** On the non-overlapping 5-day grid, a one-day rise of more than 1 usual daily move in a coin whose 30-day return is positive is followed by a 5-day return 2.89 % above the coin's normal drift (236 cases, t 3.41). The same rises in coins with a negative 30-day return are followed by +0.38 % (116 cases, t 0.43).
- **F2:** That continuation after rises in rising coins holds in 6 of 8 years (t 2.43 in 2021, 2.52 in 2024; negative in 2018 with 4 cases and in 2023 with 46 cases) and in 5 of 6 coins (XRP +7.9 %, t 1.97; ZEC +5.3 %, t 1.91; BTC, ETH and XMR +1.5 % to +1.8 %; LTC -0.8 %).
- **F3:** Within it, the gain is not cleanly graded. By rise size it is +2.6 % (t 2.41) for 1 to 1.5 usual moves, +1.1 % (t 0.65) for 1.5 to 2, and +4.7 % (t 2.36) above 2. The rise size times the 30-day depth ranks the gain only weakly (Spearman 0.07, p 0.27, 236 cases).
- **F4:** Across all grid bars, the 30-day return in usual daily moves predicts the next 5-day return above drift with r 0.060 (t 3.04, 2555 cases). The 1-day move in usual daily moves predicts it with r 0.046 (t 2.54, 2987 cases).
- **F5:** Quiet days (1-day move between -1 and +1 usual moves) in coins with a negative 30-day return are followed by a 5-day return 0.73 % below drift (928 cases, t -2.15). With a positive 30-day return they are followed by +0.34 % (930 cases, t 0.99).
- **F6:** The tested fade is too thin to judge in the data. Bounces of at least 1 usual move in coins with a negative 90-day return fall by 4.2 % over 5 days only when the 30-day return in usual moves lies between -1.5 and -0.5 (18 cases, t -2.26). With a positive 30-day return they rise 4.7 % (20 cases).
- **F7:** The book is in a position on only 4.4 % of bars. Its trades lose after fees in 5 of 6 coins: mean net trade from -1.0 % (ETH) to -7.3 % (XRP), against +0.57 % for BTC, 22 to 30 trades per coin.
- **F8:** Thursday and Friday next-day returns are higher than other days (mean +0.37 % and +0.42 %, t 3.89 and 5.23 over about 2480 days each). The edge sits mostly in 2018 and 2019 (difference t 3.37 and 5.82) and is near zero from 2021 on, so it is not a stable pattern.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth.g1_up-day-continuation-in-uptrends` (from F1, F2, F3, F4): In one coin whose 30-day return is positive, a one-day rise of at least one usual daily move is followed over the next 5 days by a further rise above the coin's normal drift. The rise is larger the higher the coin's 30-day return lies above zero in usual daily moves.
- `025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth.g2_thirty-day-momentum-over-five-days` (from F4, F5, F1): In one coin, the return over the next 5 days is higher the higher its 30-day return lies in usual daily moves. Coins below zero drift under their normal drift, and coins above it drift over.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
