---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return (Saturday close to Sunday close, measured against its own 20-day daily volatility) is reversed over the next 2 days, and the larger the Sunday move, the larger the reversal, the more so the lower its Saturday and Sunday volume was against its usual 30-day volume.
Consequence: A trader fading Sunday moves in both directions, and fading them hardest after thin weekends, would be in the market far more often and on the cases that reverse most.
Why:
- F1: The book barely earns because it holds a position on only 12.4% of days and with a small size (mean allocation 0.37 on the 2665 active Sundays), so its mean daily return is 0.00006 against 0.0015 for holding the coins, even though each active case gains 0.0017 per bar after a mean fee of 0.00043.
- F2: The weekend reversal in this data sits mostly on the side the book does not trade: after the 2589 Sunday rises, the next 2-day return is 1.09% below the coin's usual 2-day return (t -7.08), while after the 2665 Sunday falls it is only 0.23% above it (t 1.58).
- F4: The reversal is graded by weekend volume as the brief says: the slope of the excess 2-day return on the volatility-scaled Sunday return is -0.0183 (t -6.04, n 1302) in the lowest tercile of weekend volume against its 30-day average, -0.0090 (t -3.11) in the middle tercile and -0.0016 (t -0.82) in the highest.
- F5: Over all Sundays, the volatility-scaled Sunday return predicts the next 2 days with a slope of -0.0058 (t -4.39, n 4320), but the 2-day weekend return predicts nothing (slope 0.0001, t 0.09), so the information lies in the Sunday bar itself.
