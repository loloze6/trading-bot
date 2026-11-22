---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a day on which a coin rises on volume below its 30-day average, it gives back part of the rise over the next three days. The thinner the volume against its average and the larger the 1-day rise, the larger the give-back.
Consequence: A rise on thin volume is a reason to refuse a long, or to lean short, over the next three days.
Why:
- F4: A rise on thin volume gave part of itself back over the next three days. In the bottom quartile of 1-day volume and the top tercile of 1-day return, the 3-day excess was −0.160 of a usual move (t −5.0, 652 cases). Across volume quartiles 0 to 3 it rose steadily: −0.160, −0.047, +0.010, +0.061.
- F2: The rebound after a heavy-volume fall grows with the volume. Across 1-day volume quartiles 0 to 3, the next-day excess after a falling day was −0.042, −0.008, +0.012 and +0.171. In a regression of the 3-day excess on log volume ratio, bar return and their interaction on down bars, the interaction has coefficient 0.052 (t 4.6, about 11 900 cases).
