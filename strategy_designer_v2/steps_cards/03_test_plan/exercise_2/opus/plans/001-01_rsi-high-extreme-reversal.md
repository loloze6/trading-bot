---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: The horizon is 5 bars. Take the bars whose forecast is in the most negative decile (the highest RSI readings). On at least 2 of the 3 coins, the coin's 5-bar forward return after those bars is below its unconditional mean 5-bar return, with a t-stat at or below -2. The gap is also wider than the one after bars with a forecast of zero or near zero (RSI at or below 50), measured before costs. As a cross-check, the strategy's 5-bar forward return per unit of short position grows with the size of the short position.
Reject: On at least 2 of the 3 coins, the 5-bar forward return after the most negative forecast decile is at or above the coin's unconditional mean 5-bar return. That would mean no reversal, or continuation, after high RSI.
Inconclusive: The three coins disagree in direction (for example one coin reverts while the others do not), or the excess forward return after the top decile has the expected sign but |t| < 2 on two or more coins.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, a short whose size grows with the square of RSI's standardised distance above 50". Moderate readings above 50 also hold small, damped shorts, and there is no fixed extreme threshold or hold period. Only the high-extreme (reversal-down) side of the brief is tested. Low readings stay flat.
