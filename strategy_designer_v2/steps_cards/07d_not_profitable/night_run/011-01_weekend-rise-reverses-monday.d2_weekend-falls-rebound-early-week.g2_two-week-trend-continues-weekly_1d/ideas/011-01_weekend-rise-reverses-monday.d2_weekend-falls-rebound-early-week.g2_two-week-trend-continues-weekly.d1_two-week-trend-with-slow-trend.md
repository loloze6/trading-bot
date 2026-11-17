---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 14-day return scaled by its 20-day volatility is followed by a move in the same direction over the next 7 days, larger the larger that scaled return, only while the coin's 60-day return points the same way as its 14-day return.
Consequence: Side with the two-week trend only when the two-month trend agrees, and refuse two-week shorts in a coin that is still up over two months.
Why:
- F1: The book's yearly return is 0.151 and its deepest fall is −0.466, which gives the failing Calmar of 0.3246; the deepest falls inside single windows reach −0.39 to −0.47 (w9, w10), and the book loses in 11 of 24 windows.
- F2: The short leg loses money: its mean daily return is −0.000503 (t = −2.00 over 8,755 coin-days), against +0.001656 for the long leg (8,579 coin-days). The short leg's timing part is only +0.000027, and its market part is −0.000530, so shorting a rising market costs more than its timing earns.
- F3: The falls come from the shorts. On days when the book is more than 15% below its peak, the short leg contributes −0.000843 a day and the long leg −0.000064, and 53.6% of positions are short then, against 46.9% at other times. Summed over all days, the short leg loses 0.72 while the long leg gains 2.37.
- F4: The coin's own 60-day return sorts the shorts:
- F5: Longs pay most when the coin's 60-day return is moderately up (0.045 to 0.463): a mean of 0.00437 and 0.00424 a day, with timing of 0.0035. They earn far less when the 60-day return is flat (timing −0.000055) or extremely high (timing −0.000468).
- F6: Two rough recomputations of the book point the same way:
