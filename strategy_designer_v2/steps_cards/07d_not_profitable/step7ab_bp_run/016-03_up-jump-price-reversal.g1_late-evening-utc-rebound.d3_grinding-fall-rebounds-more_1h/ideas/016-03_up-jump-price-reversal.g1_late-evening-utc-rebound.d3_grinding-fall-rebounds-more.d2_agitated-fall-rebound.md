---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin's hourly volatility over the last 7 days exceeds its volatility over the last 30 days, the more it rises over the next 2 days after a fall over the last 24 hours.
Consequence: Long exposure after a daily drop is worth taking in proportion to how agitated the coin's recent week has been, which ties the book's risk to the moments that pay rather than to being long almost all the time.
Why:
- F3: The grind measure barely grades what follows: the slope t is 0.91 on 4,191 cases, and the unusual move is +0.08 % per 48 hours, 0.011 of the usual 6.56 % move. That is 0.4 times the 0.19 % cost of a round trip, so most of the book's +0.35 % total move per case is the coins' drift.
- F5: The rebound after a 24-hour fall lives in agitated markets, where the coin's 7-day hourly volatility is high against its 30-day volatility. In that upper tercile the 2-day excess return is +98 bps (126 bps total, 1,044 cases), against −11 bps in the calm tercile and −23 bps in the middle one. On all position bars, the top quintile of this ratio earns 1.34 bps per bar and carries 77 % of the book's whole gain; the other quintiles earn −0.00 to 0.23 bps.
- F7: The rebound also concentrates after a deeper 7-day fall: the lowest 7-day-return tercile gives +56 bps excess over 2 days with slope t 1.45, against −27 bps for the middle tercile.
