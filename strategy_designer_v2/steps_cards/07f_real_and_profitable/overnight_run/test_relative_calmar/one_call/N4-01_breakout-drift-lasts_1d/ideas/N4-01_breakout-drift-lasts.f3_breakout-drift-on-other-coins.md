---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: ADA, SOL, DOGE, LINK, BCH, DOT
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin's daily bars, a close at its highest close of the prior 20 days is followed by a rise over the next ten bars larger than the coin's average ten-bar rise, on coins other than those whose gain came from one rally window.
Consequence: A trader would learn whether the breakout edge is general or a by-product of a single coin's rally before sizing it across a book.
Why:
- F1: The book's compounded gain rests on one coin-window. Trades' summed net log return is 19.44, but without ZEC in w24 it is -0.31. Eight of the ten best trades (net +336% to +1159%, held 22–121 days) are ZEC w24, and the top 10 trades carry 41% of the summed net trade return.
- F4: Two of six coins lose. LTC's net log sum is -11.40 and XMR's is -12.64, against ETH +16.47 and XRP +12.00. Per coin, the non-overlapping 10-bar excess return after new 20-day highs has no t above 2 (XRP 1.90 on 38 events; BTC -0.77 on 51; XMR -0.33 on 52).
- F6: Fees are small in simple terms but large in compounding terms. They take 2.3% of the summed gross trade return but 14.5% of the gross log return (22.73 to 19.44). The win rate is 41%, and the median trade is negative in every volatility tercile.
