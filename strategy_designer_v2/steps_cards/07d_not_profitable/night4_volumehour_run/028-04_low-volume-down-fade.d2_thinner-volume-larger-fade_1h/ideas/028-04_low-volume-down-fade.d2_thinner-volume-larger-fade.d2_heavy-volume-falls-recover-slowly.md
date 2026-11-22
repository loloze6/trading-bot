---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
line: 7.d not profitable
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume above its 30-day hourly average, the price recovers part of that fall over the next two days; the further that hour's volume lies above its average, the larger the recovery.
Consequence: A heavy-volume hourly sell-off is a reason to buy for a two-day hold, not to follow it down, and a thin-volume fall is a reason to stay out.
Why:
- F1: Fees, not the forecast, sink the book: summed over both coins and all windows, the position's gain before costs is +8.54 (summed bar gains), the book's net log return is −2.39, and turnover of 17,030 times the book at 0.055 % per side costs about 9.37. Per 6-hour case the total move is +0.074 % (unusual +0.040 %, t 2.48, 17,093 cases), only 0.6 of the 0.11 % cost of a trade, and the book trades 5.4 times a day.
- F4: The plan's volume grading runs the wrong way.
- F5: Across all long cases, fall depth grades the 48 h recovery: the deepest quintile (mean −2.4 standard units) gives +0.25 % (t 2.39), while the shallowest quintile (−0.48) gives −0.24 % (t −2.69). Shallow falls, which a cubic dead zone still trades, therefore lose over two days.
