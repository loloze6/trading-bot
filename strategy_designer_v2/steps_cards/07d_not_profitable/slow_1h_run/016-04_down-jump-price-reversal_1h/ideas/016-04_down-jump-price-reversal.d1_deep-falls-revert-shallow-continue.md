---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 3 days, the more of that fall it wins back over the next 3 days, and the smaller the fall, the more the coin keeps drifting lower over those 3 days.
Consequence: A trader would lean long only into deep 3-day falls, sized by the depth of the fall, and would refuse longs after shallow declines that the jump share wrongly favours.
Why:
- F4: The top-3-losses share is mostly an inverse of the fall's size (correlation of log share with log fall size -0.90), so a high share mostly marks a small fall: the top share quintile had excess 72-bar return -0.0105 (t -2.95, n=534) against +0.0009 in the bottom quintile.
- F5: The size of the 3-day fall grades what follows the other way round from the forecast: the biggest-fall quintile (falls of 8.7% to 51%) won back +0.0060 in excess over the next 72 bars, while the smallest-fall quintile (falls under 1.3%) lost a further -0.0115 (n=533 to 534 each).
- F3: Even before fees there is almost nothing to harvest: the forecast was positive on every active bar (no short side), and the strongest bucket (forecast above 5, n=1898 fallen grid cases) had a mean excess 72-bar return of -0.0031 (t -1.69), the opposite sign to the idea.
