---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin whose 30-day return is positive, a one-day rise of at least one usual daily move is followed over the next 5 days by a further rise above the coin's normal drift. The rise is larger the higher the coin's 30-day return lies above zero in usual daily moves.
Consequence: A trader would buy sharp up days in coins that rose over the past month rather than fade them, and lean harder the stronger the month's rise.
Why:
- F1: On the non-overlapping 5-day grid, a one-day rise of more than 1 usual daily move in a coin whose 30-day return is positive is followed by a 5-day return 2.89 % above the coin's normal drift (236 cases, t 3.41). The same rises in coins with a negative 30-day return are followed by +0.38 % (116 cases, t 0.43).
- F2: That continuation after rises in rising coins holds in 6 of 8 years (t 2.43 in 2021, 2.52 in 2024; negative in 2018 with 4 cases and in 2023 with 46 cases) and in 5 of 6 coins (XRP +7.9 %, t 1.97; ZEC +5.3 %, t 1.91; BTC, ETH and XMR +1.5 % to +1.8 %; LTC -0.8 %).
- F3: Within it, the gain is not cleanly graded. By rise size it is +2.6 % (t 2.41) for 1 to 1.5 usual moves, +1.1 % (t 0.65) for 1.5 to 2, and +4.7 % (t 2.36) above 2. The rise size times the 30-day depth ranks the gain only weakly (Spearman 0.07, p 0.27, 236 cases).
- F4: Across all grid bars, the 30-day return in usual daily moves predicts the next 5-day return above drift with r 0.060 (t 3.04, 2555 cases). The 1-day move in usual daily moves predicts it with r 0.046 (t 2.54, 2987 cases).
