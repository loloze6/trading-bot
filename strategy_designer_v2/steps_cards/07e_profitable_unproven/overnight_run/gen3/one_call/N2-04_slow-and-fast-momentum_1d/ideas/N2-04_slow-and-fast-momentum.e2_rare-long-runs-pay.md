---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20- and 60-day returns are both positive, the rise above its average comes mostly from a few runs that last more than 20 days. These runs are larger in the more speculative coins such as ZEC and XRP.
Consequence: Keep momentum positions on through long runs instead of taking profits early, because the many short entries lose and the few long holds pay for them.
Why:
- F4: The profit comes from a few long, large trades: the top 10 of 2559 trades give 7290 of 14618 summed net percent (50%), and 21 of the top 25 are ZEC (11 trades, 7407) or XRP (10 trades, 1871). The win rate is 42% and the median trade is −1.14%.
- F5: By duration, trades held 20 days or more earn 18578 summed percent over 398 trades, while trades shorter than 10 days lose 5534 over 1765 trades. The book cuts many false starts and rides a few long runs.
- F1: The book earns from timing, not only from the coins' drift: it held about 30–38% of bars, and its return while held beat drift × exposure on all six coins (timing excess ZEC 5.73, ETH 4.01, BTC 3.57, XRP 2.63, LTC 0.78, XMR 0.66). Held days returned 0.00176 per day above each coin's mean (t 2.56, n 5886 daily bars). Over non-overlapping 5-bar blocks, held blocks returned +0.0081 above the coin mean (t 2.21, n 1164) and flat blocks returned −0.0039 (t −1.80, n 2255).
