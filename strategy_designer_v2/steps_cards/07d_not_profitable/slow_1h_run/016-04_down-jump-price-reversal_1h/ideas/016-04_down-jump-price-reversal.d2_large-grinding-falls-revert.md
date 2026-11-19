---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger the share of that fall that came from its few biggest hourly losses, the more of the fall the coin wins back over the next 3 days, except that among large 3-day falls the more evenly the fall was spread across the hours, the more the coin wins back over the next 3 days.
Consequence: A trader buying 3-day falls would favour large falls that ground down steadily over large falls made in a few violent hours.
Why:
- F6: Among the biggest third of falls, the falls least concentrated in their 3 worst hours won back the most, +0.0156 excess over the next 72 bars, against -0.0009 and -0.0002 for the more jump-made ones; in the smallest third of falls every share tercile kept falling (-0.0120, -0.0043, -0.0091).
- F5: The size of the 3-day fall grades what follows the other way round from the forecast: the biggest-fall quintile (falls of 8.7% to 51%) won back +0.0060 in excess over the next 72 bars, while the smallest-fall quintile (falls under 1.3%) lost a further -0.0115 (n=533 to 534 each).
- F4: The top-3-losses share is mostly an inverse of the fall's size (correlation of log share with log fall size -0.90), so a high share mostly marks a small fall: the top share quintile had excess 72-bar return -0.0105 (t -2.95, n=534) against +0.0009 in the bottom quintile.
