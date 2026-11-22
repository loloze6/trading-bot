---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close is to its 30-day closing high, the more the coin rises over the next 10 days, with the largest rise following closes at the high itself.
Consequence: A trader can buy coins closing at or just under their monthly high and should refuse to short them, rather than spread bets across the whole range.
Why:
- F1: The tested relation sits almost entirely at the top of the 30-day range. Closes in the top fifth of the range (position 0.78 to 1) were followed by +3.03 % over 10 days beyond the coin's mean (t 2.36, 252 non-overlapping cases). Every other fifth was below the mean, from -0.38 % (t -0.43) at the bottom to -0.96 % (t -1.04) in the middle. Coins near their 30-day low did not keep falling.
- F2: Closes within 1.8 % of the 30-day closing high were followed by +3.58 % over 10 days beyond the mean (t 2.44, 210 cases). The next five sixths of distance from the high ranged from -1.33 % to +0.66 %, all with |t| < 1.6. The same top sixth measured in the coin's daily-volatility units gave +3.14 % (t 2.12). For the 60-day high it gave +3.23 % (t 2.43, 138 cases).
- F3: Bars that closed on a new 30-day closing high were followed by +4.69 % over 10 days (t 2.28, 137 cases). The effect fades within days: one to two days after the high it was -0.84 % (t -0.81), and from 5 to 30 days after it was -1.23 % to -0.20 %. This finding is partly carried by one coin: XRP contributed +22.9 % (t 2.24, 18 cases), against BTC's +2.9 % (t 1.66) and +1.2 % to +2.9 % in the other coins.
- F9: The tested cost of a trade is 0.19 %. The move per case in the top fifth of the range (+3.03 %, F1) and at new highs (+4.69 %, F3) is 15 to 25 times that cost. The tested idea's average over all cases is only 0.33 %.
