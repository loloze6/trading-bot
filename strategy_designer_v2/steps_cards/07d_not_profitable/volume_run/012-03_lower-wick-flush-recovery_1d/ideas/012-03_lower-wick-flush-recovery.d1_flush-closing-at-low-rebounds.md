---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the closer the close sits to the bar's low (the shorter the lower wick as a share of the bar's high-to-low range), the larger the price rise over the next 1 day.
Consequence: A trader buying liquidation flushes should take the most size on bars that closed at their lows and the least on bars that already recovered within the bar.
Why:
- F1: The book loses because it sizes against its own edge: its position grows with the wick (mean allocation 0.80 in the top wick tercile against 0.11 in the bottom), but over 220 independent flush events the next-day return falls as the wick share rises (slope −0.073, t −2.51), and the 3-day slope is flat (t −0.22), so the correlation of position with next-day return is −0.20.
- F2: The flush rebound itself exists and is short: across 310 flush bars the mean next-day return is +1.19% (t 2.96), while by 5 days it is +0.11% (t 0.19). An equal-size long on the 220 independent events would have summed +0.56; the book's wick-sized position summed −0.51.
- F3: On a down bar the lower wick is the close's position in the bar's range (the wick and close-location regressions are identical), so a long wick means the close sat near the bar's high. Next-day return falls from +1.65% in the low-wick tercile to −0.50% in the high-wick tercile: the flushes that closed at their lows rebound most.
