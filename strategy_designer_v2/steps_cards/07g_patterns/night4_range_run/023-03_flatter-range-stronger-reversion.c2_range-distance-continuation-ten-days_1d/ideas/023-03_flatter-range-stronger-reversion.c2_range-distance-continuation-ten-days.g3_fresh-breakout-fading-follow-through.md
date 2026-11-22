---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin has closed above its 30-day closing high on a given day, the larger its rise over the next 10 days, with the effect fading over the days after the high.
Consequence: A trader can act on a fresh monthly breakout on its own day, and should not chase a high already a few days old.
Why:
- F3: Bars that closed on a new 30-day closing high were followed by +4.69 % over 10 days (t 2.28, 137 cases). The effect fades within days: one to two days after the high it was -0.84 % (t -0.81), and from 5 to 30 days after it was -1.23 % to -0.20 %. This finding is partly carried by one coin: XRP contributed +22.9 % (t 2.24, 18 cases), against BTC's +2.9 % (t 1.66) and +1.2 % to +2.9 % in the other coins.
- F2: Closes within 1.8 % of the 30-day closing high were followed by +3.58 % over 10 days beyond the mean (t 2.44, 210 cases). The next five sixths of distance from the high ranged from -1.33 % to +0.66 %, all with |t| < 1.6. The same top sixth measured in the coin's daily-volatility units gave +3.14 % (t 2.12). For the 60-day high it gave +3.23 % (t 2.43, 138 cases).
