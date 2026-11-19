---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.b inconclusive
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen modestly over the past 3 days, the smaller the share of its 3-day hourly price movement made in its three largest hours, the more the coin keeps rising over the next 3 days.
Consequence: A modest rise spread over many hours, rather than one made in a few violent hours, is a reason to hold a long for several days.
Why:
- F6: The share of the 72h hourly absolute move made in the 3 largest hours (lower means more grind) is weaker over all up moves. Low-minus-high concentration is +0.0064 (t 1.64, n 2865).
- F7: That concentration effect lives in small and mid rises and vanishes in large ones. It is +0.0118 (t 2.76, n 1910) on small and mid rises together, +0.0135 (t 2.26) on small, +0.0106 (t 1.71) on mid and -0.0001 (t -0.01) on large. Within small and mid rises it is positive in 5 of 6 coins (LTC +0.0217, t 2.07; ETH -0.0039).
- F8: Volume evenness and price-path grind are largely different measures. The tested forecast has a rank correlation of only -0.135 with the top-3-hour concentration. So the test measured the brief's "grind" through volume, while the effect shows through the shape of the price path.
