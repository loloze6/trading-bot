---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 14-day rise scaled by its 20-day volatility is followed by a further rise over the next 7 days, larger the larger that scaled rise.
Consequence: Over a one-week horizon, buy coins after strong volatility-scaled two-week rises rather than shorting after two-week falls.
Why:
- F2: The short leg loses money: its mean daily return is −0.000503 (t = −2.00 over 8,755 coin-days), against +0.001656 for the long leg (8,579 coin-days). The short leg's timing part is only +0.000027, and its market part is −0.000530, so shorting a rising market costs more than its timing earns.
- F3: The falls come from the shorts. On days when the book is more than 15% below its peak, the short leg contributes −0.000843 a day and the long leg −0.000064, and 53.6% of positions are short then, against 46.9% at other times. Summed over all days, the short leg loses 0.72 while the long leg gains 2.37.
- F6: Two rough recomputations of the book point the same way:
