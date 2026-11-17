---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell on Sunday (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) rises over the next 2 days, and the larger the Sunday fall, the larger the rise, only while the coin's 20-day daily volatility is high against its own past year.
Consequence: A trader should buy Sunday falls mainly in turbulent periods and leave them alone in calm ones, where they do not rebound.
Why:
- F3: The sizing puts its weight where the rebound is weakest. In the lowest-volatility tercile, Sunday falls are followed by a -0.25% excess 2-day return (t -1.20) while the allocation is at its highest, 0.51. In the highest-volatility tercile the excess is +1.69% (t 4.71, n 690) but the allocation is only 0.24.
- F6: The fall side alone does not grow with the size of the fall: the forecast quartiles give excess 2-day returns of -0.34%, +0.23%, +0.76% and +0.28%, and the slope stays below t 1 inside every volatility tercile. The tested slope therefore had t of only 1.12.
