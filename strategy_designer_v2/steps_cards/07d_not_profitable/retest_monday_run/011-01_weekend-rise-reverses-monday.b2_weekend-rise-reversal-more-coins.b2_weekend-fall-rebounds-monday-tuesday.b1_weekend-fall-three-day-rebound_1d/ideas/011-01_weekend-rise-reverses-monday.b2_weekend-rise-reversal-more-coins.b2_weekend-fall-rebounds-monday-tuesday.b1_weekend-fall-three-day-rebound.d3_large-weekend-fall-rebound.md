---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) by a large multiple of its usual daily move rises over the next 3 days (Monday to Wednesday). The rise grows with how many usual daily moves the weekend fall spans, and is carried by the largest falls.
Consequence: Trade only the weekend falls that are large against the coin's usual daily move, and size by that multiple rather than by recent volatility.
Why:
- F5: The book's gain comes from the large falls. Cases with a forecast of 8 to 12 and 12 to 20 summed +3.81 and +5.52 of the book's +10.9 of case returns after costs. Forecasts of 2 to 8 summed about +1.1 across 947 cases, with excess returns of -0.25 %, +0.76 % and -0.62 %. Keeping only forecasts of 8 or more lifted the weekly-chain Calmar to 1.03.
- F6: The losing years were 2018 (-3.00 % mean excess, 107 cases) and 2022 (-1.05 %, 375 cases). Within the w1 to w9 fall, the large-forecast cases still earned +0.88 % (329 cases) while the small ones earned -0.10 % (399 cases).
- F2: Volatility targeting sized the book against the effect. Across quartiles of 20-day daily volatility at the Sunday close, the mean position fell from 0.56 to 0.32 while the mean excess 3-day return rose from +0.14 % to +3.59 % (444 cases per quartile). In w1 to w9 the two calmest quartiles lost -0.39 and -0.61 in summed case returns and the most volatile one gained +1.37. A fixed position per case gave a weekly-chain Calmar of 1.44 against 0.65 as tested; this is an approximate chain of case returns after a 0.22 % cost, not the daily book.
