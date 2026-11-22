---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days, except when the 30-day return is large against the coin's own usual 30-day move: there, the larger that excess, the smaller the rise that follows.
Consequence: A trader leans long hardest on moderate monthly strength at the high and cuts the long as the rally becomes extended, where the book's worst bars came from.
Why:
- F1: The Calmar of 0.51 fails because one fall is far deeper than the rest: the chain of daily returns falls 51.6 % over 888 days (w1 to w11, book −50.7 % while the coins fell −59.6 %), against a yearly return of 26.3 %; the next deepest falls are −33.0 % (w12–w16), −19.1 % (w19–w21) and −18.5 % (w21–w23).
- F4: The long gain is hump-shaped in the 30-day return. Long bars in the 30-day-return quintiles at +14 % and +27 % earn +0.29 % and +0.45 % per bar. The top quintile, at +63 %, earns only +0.06 % per bar with the widest spread (std 3.98 %).
- F5: The book's worst bars are longs taken after an extended rally at the high. The worst 5 % of active bars include 512 longs summing −32.2, with a mean 30-day return of +36 %, a mean distance of only 4.2 % below the 60-day high, and a mean 5-day return of +11 %. These are the bars the forecast sizes largest (mean |allocation| 1.12 in the nearest-to-high quintile).
- F6: Longs inside the deep falls (the book more than 10 % below its peak) earn +0.12 % per bar over 5638 bars, against +0.31 % outside them. Inside those falls their mean 30-day return is lower (+14 % vs +31 %) and they stand further from the high (12.3 % vs 8.4 %). The longs taken in the falls ride weaker, older rallies.
