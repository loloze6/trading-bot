---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's volatility over the past day is high relative to its past 30 days, an hourly fall far larger than its typical hourly move is followed by a rebound over the next two hours. The higher the recent volatility and the larger the fall, the larger the rebound.
Consequence: A trader would buy sharp hourly drops mainly in turbulent stretches, where the bounce is several times larger than in calm ones.
Why:
- F1: Large hourly falls rebound strongly while large hourly rises barely fade. Over the next 2 hours (non-overlapping, excess over the coin's drift), falls beyond -4 usual moves are followed by +35.3 bp (t 5.55, n 2304) and falls of -2.5 to -4 by +16.1 bp (t 5.59, n 5078). Rises of 2.5 to 4 and beyond 4 are followed by only -2.7 bp (t -0.93) and -5.4 bp (t -1.02). The tested short-the-rise idea sits on the weak side of this asymmetry.
- F4: The rebound grows with the recent volatility regime. After falls beyond -2.5 usual moves, the 2-hour excess is +44.7 bp (t 6.79) in the top tercile of 24-hour versus 30-day volatility and +7.3 bp (t 2.33) in the bottom tercile. The reversal of big moves in both directions follows the same order: -16.2 bp (t -7.13) in the top volatility quartile against +6.4 bp (t 1.49) in the bottom.
- F5: The rebound after large falls holds across every coin and most years.
