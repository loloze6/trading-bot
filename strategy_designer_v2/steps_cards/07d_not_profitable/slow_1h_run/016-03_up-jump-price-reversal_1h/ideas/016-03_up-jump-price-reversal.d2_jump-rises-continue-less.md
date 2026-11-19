---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise that came from its few biggest hourly gains, the smaller the coin's further rise over the next 3 days.
Consequence: A trader would scale down long exposure after rises carried by a few violent hours, rather than short them, because those rises still drift up only less.
Why:
- F2: After a 3-day rise the coin kept rising in absolute terms at every forecast level on the 72-bar grid: +0.39% when the forecast was -10 to -20 (n=2489) and +1.49% when it was -5 to -10 (n=408). The confirmed slope is a difference in how much the coin rises, not a fall that a short can collect.
- F3: The forecast is close to saturated, so the short is close to a fixed full position on every rising bar. On trending bars its mean is -14.5 and its median -13.8, a quarter of them sit at the -20 cap, and 2489 of 2916 grid cases fall in the -10 to -20 bucket. The share's grading is therefore almost absent from the position size.
- F4: The short loses more than the market's rise alone explains. For BTC the gross position gain is -0.000061 per bar, of which only -0.000028 comes from the market's own drift. Timing is also negative on every coin except XMR, whose gross is +0.000008 per bar against -0.000021 from drift.
