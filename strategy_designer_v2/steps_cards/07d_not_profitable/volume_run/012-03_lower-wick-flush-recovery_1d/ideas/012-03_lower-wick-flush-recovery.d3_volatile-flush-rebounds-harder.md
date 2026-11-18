---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the higher the coin's 20-day volatility of daily returns before the bar, the larger the price rise over the next 1 day.
Consequence: Liquidation-flush rebounds pay mainly in already turbulent coins, so size on the turbulence rather than on the wick.
Why:
- F2: The flush rebound itself exists and is short: across 310 flush bars the mean next-day return is +1.19% (t 2.96), while by 5 days it is +0.11% (t 0.19). An equal-size long on the 220 independent events would have summed +0.56; the book's wick-sized position summed −0.51.
- F5: The rebound grows with the coin's prior 20-day volatility (slope on next-day return t 7.76, on 3-day return t 5.11, 220 events) and with the volume ratio (next-day t 2.67).
