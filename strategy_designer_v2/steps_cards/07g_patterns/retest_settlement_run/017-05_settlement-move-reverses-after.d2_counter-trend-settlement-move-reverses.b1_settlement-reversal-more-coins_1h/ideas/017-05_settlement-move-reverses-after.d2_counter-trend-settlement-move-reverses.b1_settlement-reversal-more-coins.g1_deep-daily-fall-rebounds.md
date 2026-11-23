---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 24 hours, the higher its return over the next 24 hours, and this rebound is larger when the coin's volatility over the past day is high compared with its past week.
Consequence: A trader buys a coin after a deep 24-hour fall, more so when the fall came with a surge in volatility, and refuses to short into such falls.
Why:
- F1: The biggest drops in a coin's 24 hours are followed by a rebound, and the rebound is the one move here that is larger than a trade's cost. On the 24-hour grid, in the bottom fifth of 24-hour falls, the next 24 hours run +0.141 of a usual 24-hour move above the drift (t 6.45, 3591 cases). Averaged across coins per day it is +0.106 (t 2.86, 934 days). It is positive in 7 of 8 years; 2022 is the exception at -0.053. The other four fifths of falls give +0.021 to -0.035. At roughly 5.4 % for a usual 24-hour move (from the 3.12 % 8-bar move), +0.141 is about 0.76 % per case, more than three times the 0.22 % trade cost.
- F2: The 24-hour reversal is concentrated where short-term volatility is high. In the top third of 24-hour over 168-hour volatility, the 24-hour return continues by -0.037 of a usual move (t -3.25, 11503 cases). In the bottom third it is +0.001 (t 0.15).
- F7: The losses sit on the short side. Short trades lose -0.51 % before fees (34024 trades), while long trades gain +0.22 % (34438 trades). Before costs the book earns only 0.055 bp per coin-hour, against a yearly return of -16.1 %.
