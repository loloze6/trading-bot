---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall, the larger the rise. The rise is larger the further the coin had already fallen over its past 20 days.
Consequence: Favour buying weekend falls that come after a 20-day decline, and refuse those that come after a 20-day rise.
Why:
- F4: The rebound concentrates after coins that were already down over the prior 20 days, and that condition alone loses. Sunday falls in the lowest quartile of 20-day return gave +2.54 % excess (t 5.72, 548 cases), the second quartile +1.48 % (t 3.18), the third -0.46 % (t -1.13). Sundays with no fall signal in the lowest quartile gave -1.49 % (444 cases). Restricting to cases below the median 20-day return raised the weekly-chain Calmar to 2.85, with a deepest fall of -9.1 % (approximate chain).
- F1: The check failed on Calmar (0.31 against 0.75). The book's deepest fall was -35.6 % over 880 days, through windows w1 to w9, while the coins' mean chain fell -45.0 % over the same span. Inside those windows the 859 Sunday cases earned a mean excess 3-day return of -0.26 % (t -0.87). The other 1356 cases earned +1.54 % (t 5.18), so the fall comes from periods where the effect was absent.
