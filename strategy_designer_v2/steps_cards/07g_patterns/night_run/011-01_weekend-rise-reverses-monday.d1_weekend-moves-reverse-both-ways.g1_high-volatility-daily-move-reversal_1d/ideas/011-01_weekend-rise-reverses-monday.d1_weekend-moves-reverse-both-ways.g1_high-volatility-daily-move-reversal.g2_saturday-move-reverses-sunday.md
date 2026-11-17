---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday (UTC) daily move reverses over the next 1 day, and the larger Saturday's return measured in its 20-day volatility, the larger the move back on Sunday.
Consequence: Fade Saturday's move into Sunday in proportion to its vol-scaled size, a weekend-specific reversal trade separate from weekday fades.
Why:
- F3: Saturday's vol-scaled move reverses on Sunday more than any other weekday's move does. Its slope is -0.150 (t -4.89, n 1578), against -0.068 (t -1.83) for Sunday and -0.053 to +0.010 for Tuesday to Friday. The Saturday slope is clearly negative in 2018, 2019, 2022 and 2024 (t -3.9, -4.9, -3.9, -3.8), near zero in 2020, 2021 and 2023, and positive in 2025 (+0.25, t 1.80).
- F6: The book is only weakly tied to the coins, with a daily correlation of 0.118. Its mean daily return is flat across weekdays, ranging from -0.0002 to +0.0011 with no weekday reaching |t| 2. So the strong Saturday reversal (F3) is not being captured separately by the strategy.
