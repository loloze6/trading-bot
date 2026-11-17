---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose on Sunday (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) falls over the next 2 days, and the larger the Sunday rise, the larger the fall.
Consequence: The short side of the Sunday fade carries most of the reversal, so a trader should short Sunday rises rather than only buy Sunday falls.
Why:
- F2: The weekend reversal in this data sits mostly on the side the book does not trade: after the 2589 Sunday rises, the next 2-day return is 1.09% below the coin's usual 2-day return (t -7.08), while after the 2665 Sunday falls it is only 0.23% above it (t 1.58).
- F5: Over all Sundays, the volatility-scaled Sunday return predicts the next 2 days with a slope of -0.0058 (t -4.39, n 4320), but the 2-day weekend return predicts nothing (slope 0.0001, t 0.09), so the information lies in the Sunday bar itself.
