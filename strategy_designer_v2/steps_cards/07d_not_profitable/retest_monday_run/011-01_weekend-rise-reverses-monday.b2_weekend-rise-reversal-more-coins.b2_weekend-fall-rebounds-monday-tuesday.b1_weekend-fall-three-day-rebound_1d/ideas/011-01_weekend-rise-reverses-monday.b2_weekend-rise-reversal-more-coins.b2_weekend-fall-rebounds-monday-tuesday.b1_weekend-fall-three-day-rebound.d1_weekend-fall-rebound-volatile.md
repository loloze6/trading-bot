---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall, the larger the rise. The rise is larger the more volatile the coin's daily moves were over the past 20 days, so the rebound is carried by the weekend falls of agitated markets.
Consequence: Buy large weekend falls at Sunday's close and hold through Wednesday, without cutting the position when recent volatility is high, because that is where the rebound is largest.
Why:
- F2: Volatility targeting sized the book against the effect. Across quartiles of 20-day daily volatility at the Sunday close, the mean position fell from 0.56 to 0.32 while the mean excess 3-day return rose from +0.14 % to +3.59 % (444 cases per quartile). In w1 to w9 the two calmest quartiles lost -0.39 and -0.61 in summed case returns and the most volatile one gained +1.37. A fixed position per case gave a weekly-chain Calmar of 1.44 against 0.65 as tested; this is an approximate chain of case returns after a 0.22 % cost, not the daily book.
- F3: The effect lives in Sundays with high volatility, and high volatility alone does not earn it. Sunday falls with 20-day volatility above the median gave +2.17 % excess over 3 days (887 cases), against +0.24 % below the median (888 cases). Sundays above the median with no fall signal gave -1.04 % (1027 cases), so the condition alone does not earn the rise. This fits the brief: a thin weekend book in an agitated market charges the largest liquidity cost.
- F1: The check failed on Calmar (0.31 against 0.75). The book's deepest fall was -35.6 % over 880 days, through windows w1 to w9, while the coins' mean chain fell -45.0 % over the same span. Inside those windows the 859 Sunday cases earned a mean excess 3-day return of -0.26 % (t -0.87). The other 1356 cases earned +1.54 % (t 5.18), so the fall comes from periods where the effect was absent.
