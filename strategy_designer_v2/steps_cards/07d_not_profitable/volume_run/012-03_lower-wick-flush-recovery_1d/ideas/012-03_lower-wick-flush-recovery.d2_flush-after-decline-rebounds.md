---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the larger the rise over the next 1 day, the deeper the coin's 20-day return was negative before the bar.
Consequence: A flush that ends a month-long decline is a rebound to buy; a flush in a coin that had not been falling is one to skip.
Why:
- F2: The flush rebound itself exists and is short: across 310 flush bars the mean next-day return is +1.19% (t 2.96), while by 5 days it is +0.11% (t 0.19). An equal-size long on the 220 independent events would have summed +0.56; the book's wick-sized position summed −0.51.
- F4: The rebound is carried by flushes that come after a 20-day decline: next-day return is +2.58% in the lowest 20-day-return tercile against −0.97% in the middle and +0.16% in the top (slope t −4.07 on 1 day, −2.11 on 3 days, 220 events). The book held less there (0.28) than in the other terciles (0.52, 0.48).
