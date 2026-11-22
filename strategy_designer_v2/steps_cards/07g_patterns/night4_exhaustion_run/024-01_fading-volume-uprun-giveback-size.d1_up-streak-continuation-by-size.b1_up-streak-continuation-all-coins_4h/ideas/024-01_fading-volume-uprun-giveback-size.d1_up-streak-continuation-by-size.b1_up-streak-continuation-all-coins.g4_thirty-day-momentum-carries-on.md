---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the more it rises over the next three days.
Consequence: A strong one-month gain is a reason to stay long for the next three days rather than fade it.
Why:
- F7: The coin's 30-day return is roughly graded with the next 18 bars, but not at the bottom. Its quintiles read -0.10 %, -1.07 % (t -5.6), -0.34 %, +0.50 % and +0.77 % (t 2.95).
- F4: Up streaks do not continue. The tested measure gave -0.02 % per case (t -0.25, 12162 cases). Among up streaks of 3 or more bars, the unusual move is not graded by size: -1.11 % to +1.32 %, every t below 2.2 in absolute value.
