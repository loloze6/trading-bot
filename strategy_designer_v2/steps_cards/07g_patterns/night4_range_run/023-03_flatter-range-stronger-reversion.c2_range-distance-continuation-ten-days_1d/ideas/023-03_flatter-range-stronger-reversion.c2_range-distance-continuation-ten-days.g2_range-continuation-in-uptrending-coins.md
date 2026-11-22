---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 60-day return is positive, the higher its daily close sits above the middle of its 30-day closing range, the more it keeps rising over the next 10 days. The larger the 60-day rise, the stronger this effect.
Consequence: A trader can lean with range position only in coins that are up over two months, and should ignore range position in coins that are down.
Why:
- F4: The idea's slope (10-day excess return on range position) depends on the coin's own 60-day return. It was 0.0387 (t 2.88, 423 cases) when the 60-day return was positive and -0.0043 (t -0.38, 404 cases) when it was negative. By size of the 30-day move it was 0.0182 (t 1.51) in the trending third and 0.0073 (t 0.73) in the flattest third.
- F1: The tested relation sits almost entirely at the top of the 30-day range. Closes in the top fifth of the range (position 0.78 to 1) were followed by +3.03 % over 10 days beyond the coin's mean (t 2.36, 252 non-overlapping cases). Every other fifth was below the mean, from -0.38 % (t -0.43) at the bottom to -0.96 % (t -1.04) in the middle. Coins near their 30-day low did not keep falling.
- F6: The relation is unstable across years. The slope was positive in 2020 (t 2.67) and 2019/2021 (t 1.22/1.56), and negative in 2018 (t -2.26), 2022 (t -1.96) and 2023 (t -2.16). By coin, only XRP (t 2.08) and ETH (t 1.73) carry it, while BTC, LTC and XMR have |t| < 0.3.
