---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 2 hours, the higher its return over the next 8 hours.
Consequence: A trader leans long after sharp 2-hour drops and avoids shorting into them.
Why:
- F3: Sharp 2-hour falls also rebound, but by less than a trade costs. On the 8-hour grid, the bottom fifth of 2-hour returns is followed by +0.035 of a usual 8-hour move over 8 hours (t 4.49, 22037 cases). The other fifths give +/-0.014 or less. In money that is about 0.11 % per case, under the 0.22 % cost.
- F7: The losses sit on the short side. Short trades lose -0.51 % before fees (34024 trades), while long trades gain +0.22 % (34438 trades). Before costs the book earns only 0.055 bp per coin-hour, against a yearly return of -16.1 %.
