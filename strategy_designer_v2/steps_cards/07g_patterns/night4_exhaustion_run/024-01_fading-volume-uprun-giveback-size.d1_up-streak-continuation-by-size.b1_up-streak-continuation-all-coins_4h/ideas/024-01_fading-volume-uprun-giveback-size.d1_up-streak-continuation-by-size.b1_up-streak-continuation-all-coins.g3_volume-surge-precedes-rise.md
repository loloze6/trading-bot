---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's 4-hour volume against its own 30-day norm, the more the coin rises over the next three days, whichever way that period closed.
Consequence: An unusually heavy-volume 4-hour period is a reason to hold the coin long for the next three days.
Why:
- F5: The bar's volume against its own 30-day norm is graded with the next 18 bars, whatever the bar's direction. Volume quintiles read -0.74 % (t -3.6), -0.53 %, -0.23 %, +0.12 % and +1.16 % (t 4.5). The top volume quartile gains +1.25 % after down bars (t 4.3) and +0.81 % after up bars (t 2.4).
- F6: The bar's high-low range in usual moves is graded the same way. Range quintiles read -0.71 %, -0.89 % (t -5.3), -0.01 %, +0.24 % and +1.15 % (t 4.45); this partly overlaps F5.
