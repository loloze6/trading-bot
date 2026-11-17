---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way spread evenly over Monday and Tuesday (the next 2 days). The reversal is larger the larger the Sunday move and the higher the coin's 20-day daily volatility, and it shows only while that volatility is high against its own past year.
Consequence: Fade Sunday moves through Tuesday's close rather than only Monday's, and put the size in high-volatility weeks rather than calm ones, so the gain per trade clears the round-trip fee.
Why:
- F1: The book earns only on Monday, while fees eat most of what the Sunday position makes. The book's mean return is 0.00090 on Mondays, -0.00043 on Sundays and about 0 on all other weekdays. The gross Sunday-to-Monday gain is 0.00135 per case (t 3.79, n 5259), against a fee of 0.00045 to enter and 0.00045 to exit. About two thirds of the gross gain goes to fees, which leaves a mean daily return of 0.000137.
- F2: The reversal lasts two days, but the book is held for one. The signed reversal is 0.00326 on Monday (t 4.13) and a further 0.00366 on Tuesday alone (t 5.14), then 0.00101 (t 1.22) on Wednesday and -0.00118 on Thursday. Keeping the same position through Tuesday would add 0.00094 per case (t 2.79) with no extra fee.
- F3: The book's size is largest where the reversal is absent. In the lowest quartile of 20-day volatility, the Monday gain is -0.00032 (t -0.39) while the mean |allocation| is 0.56. In the upper three quartiles the gain is 0.0014 to 0.0025 (t 2.0 to 3.1) at allocations of 0.25 to 0.38. The 2-day signed reversal also rises with volatility, from 0.0003 in the lowest quartile to 0.0075 in the highest.
- F4: The rise in recent volatility against 60-day volatility matters only at its top. In the top quartile of the 20/60 volatility ratio, the Monday gain is 0.00334 and the 2-day reversal is 0.0073 (t 2.86). The other quartiles give -0.0008 to 0.0012.
- F6: The effect fades over time. The 1-day reversal is 0.004 to 0.009 in 2018–2021 but only 0.0006 to 0.001 in 2022–2023 and -0.0014 in 2025, while the 2-day reversal stays positive (0.0024 to 0.0103).
