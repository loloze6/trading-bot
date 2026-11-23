---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 20-day return, measured in units of its usual daily move over the past 60 days, continues in the same direction over the next 3 days from Thursday's close, and the continuation is larger the larger that 20-day return.
Consequence: Hold the coin's 20-day trend from Thursday to Sunday, sized by its strength.
Why:
- F5: The coin's 20-day return in usual-move units predicts the next 3 days in its own direction from midweek closes, not from Sunday. Its coefficient is +0.0087 per unit from Thursday (t 10.3, 4,259 bars) and +0.0061 from Wednesday (t 6.0). From Sunday it is −0.0006 (t −0.70). These t's are inflated because the coins share the same days.
