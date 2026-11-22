---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a day on which a coin falls while trading far more than its 30-day average volume, it rises over the next one to three days. The heavier that day's volume against its average and the deeper the 1-day fall, the larger the rebound.
Consequence: A heavy-volume sell-off is a reason to lean long for the next one to three days rather than follow the fall.
Why:
- F1: After a day on which the coin fell and traded far more than usual, it rebounded. In the top quartile of 1-day volume against the 30-day average and the bottom tercile of the volatility-scaled 1-day return, the next day's excess return was +0.171 of a usual move (t 8.3, 3229 cases). The next 3 days' excess was +0.172 (t 5.2, 1051 cases), about +1.6 % against a usual 3-day move of 9.29 % and a trade cost of 0.22 %.
- F2: The rebound after a heavy-volume fall grows with the volume. Across 1-day volume quartiles 0 to 3, the next-day excess after a falling day was −0.042, −0.008, +0.012 and +0.171. In a regression of the 3-day excess on log volume ratio, bar return and their interaction on down bars, the interaction has coefficient 0.052 (t 4.6, about 11 900 cases).
- F3: The heavy-volume-fall rebound holds on most coins and years, but not in the two bear years. Its 3-day excess is positive on 18 of 19 coins (INJ −0.146, the exception) and in 6 of 8 years, with t above 2.3 in 2019, 2020, 2021, 2024 and 2025. It is negative in 2018 (−0.104) and 2022 (−0.063).
- F5: The tested volume-surge effect comes mostly from surges on falling bars. In the top quintile of the 4h volume ratio, the 3-day excess was +0.143 (t 4.2, 1165 cases) after a down bar and +0.069 (t 1.9, 1207 cases) after an up bar. In the bottom quintile it was negative on both sides: −0.094 (t −3.6) and −0.072 (t −2.8).
