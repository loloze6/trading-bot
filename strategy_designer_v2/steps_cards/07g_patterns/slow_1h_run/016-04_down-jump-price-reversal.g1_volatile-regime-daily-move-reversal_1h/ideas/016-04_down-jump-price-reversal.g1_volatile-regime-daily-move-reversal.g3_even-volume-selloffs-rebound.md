---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more evenly a coin's volume is spread across the hours of a 24-hour fall, the more the coin rises over the next 24 hours, for falls of the same size measured in units of its 7-day hourly volatility.
Consequence: Buy sharp daily drops that came on steady volume rather than drops driven by a single volume burst, and size the trade by how even the volume was.
Why:
- F5: Against the brief, falls with evenly spread volume rebound most, and falls built on a volume burst rebound least. In the lowest tercile of volume concentration (largest hour's share of 24-hour volume), bottom-fifth moves rebound 0.0080 (t 3.86, n 977); in the highest tercile they rebound 0.0006 (t 0.43, n 1,240). The regression term for scaled move × volume concentration has t +3.36, so a volume burst weakens the reversal.
- F3: The reversal is lopsided toward falls. The bottom fifth of scaled 24-hour moves is followed by +0.0041 excess over the next 24 hours (t 4.25, n 3,308), while the top fifth is followed by only -0.0019 (t -2.19, n 3,305).
