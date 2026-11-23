---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell on Sunday rises over the next 3 days. The rise is larger the more the coin had already fallen over its past 20 days, with that 20-day return measured in units of its usual daily move over the past 60 days.
Consequence: Weight a Sunday-fall buy by the depth of the coin's 20-day decline, and refuse the trade when the coin is in a 20-day rise.
Why:
- F1: The Sunday-fall rebound depends on the coin's 20-day trend. Sunday falls (more than 0.3 usual daily moves) whose 20-day return, in usual-move units, sits in the lowest fifth gain +3.05 % over the next 3 days beyond drift (t 5.85, 316 cases). The next two fifths gain +2.25 % (t 3.35) and +1.19 % (t 2.47). The top two fifths gain −0.02 % (t −0.04) and +0.60 % (t 1.00). Across all 4,264 Sundays, the Sunday return × 20-day return interaction has t 4.53.
- F2: The Sunday falls that came during a 20-day decline rebounded in all 19 coins (means +0.68 % to +8.43 %) and in every year from 2019 to 2025 (+0.20 % to +14.8 %). 2018 alone was negative (−1.31 %, t −1.04, 44 cases).
- F7: The book's gain sits on a few days. All of the book's top 2 % and bottom 2 % days fall Monday to Wednesday (58 each, mean +3.79 % and −3.20 %). The top 2 % days sum to 227 % of the book's total gain, which explains a Calmar of 0.30 despite a Sharpe of 0.71.
