---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
line: 7.d not profitable
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers part of that fall over the next two days, only while the coin's 7-day return is positive; the higher its 7-day return and the deeper that hour's fall, the larger the recovery.
Consequence: A trader buys sharp hourly falls only inside a coin that rose over the past week, holds for about two days rather than six hours, and sizes by the strength of the week's rise, so the captured move covers the cost several times over.
Why:
- F1: Fees, not the forecast, sink the book: summed over both coins and all windows, the position's gain before costs is +8.54 (summed bar gains), the book's net log return is −2.39, and turnover of 17,030 times the book at 0.055 % per side costs about 9.37. Per 6-hour case the total move is +0.074 % (unusual +0.040 %, t 2.48, 17,093 cases), only 0.6 of the 0.11 % cost of a trade, and the book trades 5.4 times a day.
- F2: The recovery grows with time where the fall comes after a 7-day rise. For long cases in the top quintile of the coin's 7-day return (mean +16 %), the unusual move is +0.155 % over 6 h (t 4.09), +0.39 % over 24 h (t 5.28) and +0.66 % over 48 h (t 6.24, about 3,220 cases), with a total move of +0.94 % over 48 h, about 8.5 times the cost. The three middle quintiles are negative over 48 h (−0.14 %, −0.23 %, −0.11 %; t −1.6, −2.8, −1.3).
- F3: Inside that top 7-day quintile, every fall-depth tercile recovers over 48 h, and the deepest falls recover more: +0.75 % (t 4.35, strength 0.127), +0.71 % (t 4.08) and +0.46 % (t 2.27) from deepest to shallowest. The 48 h effect holds in 7 of 8 years, at +0.40 % to +1.18 %; the exception is 2022, at −0.87 % (t −3.06).
- F5: Across all long cases, fall depth grades the 48 h recovery: the deepest quintile (mean −2.4 standard units) gives +0.25 % (t 2.39), while the shallowest quintile (−0.48) gives −0.24 % (t −2.69). Shallow falls, which a cubic dead zone still trades, therefore lose over two days.
