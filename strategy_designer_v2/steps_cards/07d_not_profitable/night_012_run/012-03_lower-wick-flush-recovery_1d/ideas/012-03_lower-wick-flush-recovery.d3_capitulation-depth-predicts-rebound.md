---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among daily bars that fall sharply on a volume burst, the more the coin has fallen over the prior 20 days, the larger the price rise over the next 1 to 3 days.
Consequence: A volume-burst crash that comes at the end of a long slide is a capitulation worth buying, the more so the longer the slide.
Why:
- F4: The book's daily mean is -6.8e-6 against the coins' 0.00119. It is invested on only 2.4 % of days, and 70 % of those 416 days are losses.
- F6: The rebound grows with the depth of the coin's prior fall. Flush bars in the lowest quarter of 20-day return (mean -32 %) rose 4.30 % the next day (t 2.92, n 49) and 3.69 % over 3 days (t 2.22, n 49). The other quarters rose between -0.28 % and 0.48 % the next day, all with |t| below 0.6.
