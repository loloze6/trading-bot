---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: While the coin's 30-day return is negative, an hour in which it rises far more than its typical hourly move on near-average volume is followed by a fall over the next 24 hours. The deeper the 30-day decline, the larger that fall.
Consequence: A trader would short quiet hourly rises only inside a falling month, sized by how far the month has fallen, and would stay out of them in rising markets.
Why:
- F4: Most of the gross loss is being short a coin that drifts up. The book is short on 54 % of bars at a mean position of -0.52. Per bar, the market's own rise costs it -0.17 bp on BTC and -0.16 bp on ETH, while timing adds only +0.05 bp on BTC and -0.07 bp on ETH. Fees add about 0.44 and 0.33 bp per bar on top (turnover 0.080 and 0.060 per bar).
- F5: Shorting pays only in a falling month. On bars held short, the gain is +0.23 bp per bar (timing +0.46 bp) in the lowest tercile of the coin's 30-day return. It is -0.74 bp in the middle tercile and -0.57 bp in the top tercile.
- F3: Larger forecasts do not do better. Trades lose -0.30 %, -0.41 %, -0.28 % and -0.38 % gross across entry-forecast bands 0–3, 3–8, 8–15 and 15–20. The verdict's larger-forecast half also beat the smaller half by -0.026 %, so the grading the idea claims is absent.
