---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
Consequence: A trader should size an upward four-hour breakout by how quiet the preceding week was against the past two months, rather than by how narrow the two-day stretch itself was.
Why:
- F2: The quietness of the past week is the part of the idea that does grade the move, though weakly. Over the 2,733 breakouts (first per 18-bar cell), those with the quietest 7-day/60-day range ratio (lowest quarter, below 0.77) end 18 bars later +0.69 % above drift (t 2.00, strength 0.087). The loudest quarter (above 1.15) ends −0.36 % (t −0.87, strength −0.059). The rank correlation of the ratio with strength is −0.068 (p 0.0004), and the slope on its within-coin rank is −1.27 % (t −2.16). The bets show the same pattern: quietest quarter +0.70 % (t 2.00, 661 cases), loudest −0.41 % (t −1.02).
- F3: The other two parts of the forecast predict nothing. The stretch's narrowness against the 30-day range has a rank correlation of 0.007 with strength (p 0.70), and the size of the break above the 12-bar high has 0.010 (p 0.61). Their multiplication only adds noise to the quiet-week factor.
- F1: The test could not measure its own grading, because the forecast is pinned at its cap: 87 % of the 3,101 bets enter at a forecast of 20, and the median, the 25th percentile and every quantile above them equal 20. The split at the median therefore left 0 cases in the high-forecast half and 3,102 in the low half, so the supporting check returned nothing.
- F5: Coins differ, and on its full cases the idea is too small to trade. Over all bets the move is +0.18 % above drift (t 1.13, 3,102 cases), 0.9 times the 0.19 % round-trip cost. By coin it ranges from LTC −0.54 % (t −1.56) to XRP +0.64 % (t 1.10). In the quietest-week quarter the unusual move is about +0.69 %, about 3.6 times the cost. On that quarter, five of the six coins are positive (XMR +1.34 %, t 2.15) and LTC is the exception at −0.45 %.
