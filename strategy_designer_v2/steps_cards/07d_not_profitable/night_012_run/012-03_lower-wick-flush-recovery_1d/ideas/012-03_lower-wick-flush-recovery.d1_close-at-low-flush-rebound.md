---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among daily bars that fall sharply on a volume burst, the closer the close sits to the bar's low, as a share of the bar's high-to-low range, the larger the price rise over the next 1 day.
Consequence: A flush that closes at its low, with selling still unabsorbed inside the bar, is the one to buy for a one-day snap-back, and a flush that already recovered into its range is the one to skip.
Why:
- F1: The forecast sizes the position against the effect: on the 246 flush bars, those closing nearest their low (bottom quarter of close-in-range, mean 0.06) rose 2.96 % the next day (t 3.04, n 62) yet got a mean allocation of only 0.0099, while those closing nearest their high (top quarter, mean 0.48) fell 0.22 % the next day (t -0.30, n 62) with the largest allocation, 0.485.
- F2: Across the flush bars, a higher close-in-range comes with a lower next-day return (Spearman -0.197) and no different 3-day return (Spearman -0.005), which matches the verdict's 3-bar slope t of 0.77.
- F3: The book holds the position only on the flush bar itself (mean allocation 0.24 on the bar, 0.015 on the next), so it collects only the 1-day move. It earned 0.011 in summed next-day gains against about 0.120 in summed entry and exit fees.
