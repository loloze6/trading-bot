---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the smaller the share of that rise that came from its few biggest hourly gains (a grind of many small hourly steps), the more the coin keeps rising over the next 3 days.
Consequence: A trader would go long into grinding 3-day rises and size the position by how evenly the rise was spread across hours, instead of shorting jump-made rises that still drift up.
Why:
- F2: After a 3-day rise the coin kept rising in absolute terms at every forecast level on the 72-bar grid: +0.39% when the forecast was -10 to -20 (n=2489) and +1.49% when it was -5 to -10 (n=408). The confirmed slope is a difference in how much the coin rises, not a fall that a short can collect.
- F6: Rises that were the most grind-like were followed by the largest further gains. Grid cases with forecast near 0 rose +3.06% over the next 72 bars (n=12, a thin sample), against +1.49% for -5 to -10 and +0.39% for -10 to -20, so forward returns fall steadily as the jump share grows.
- F1: The book is short on about half of all bars and never long (share_short 0.46–0.52, share_long 0.0 on every coin), so it loses as the coins rise, with mean daily returns from -0.0015 (XMR) to -0.0027 (ETH) while holding the coins earned +0.0007 to +0.0016 a day.
