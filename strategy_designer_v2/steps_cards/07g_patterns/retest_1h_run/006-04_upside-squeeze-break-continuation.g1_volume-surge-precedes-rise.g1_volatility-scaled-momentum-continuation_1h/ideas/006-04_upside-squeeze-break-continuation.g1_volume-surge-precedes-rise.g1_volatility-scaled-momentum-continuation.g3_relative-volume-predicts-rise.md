---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's volume over the last day relative to its own 20-day average volume, the more its price rises over the next 3 days relative to its usual 3-day return.
Consequence: A coin trading on unusually heavy volume is a reason to lean long for the next few days, and unusually thin volume is a reason to stay out.
Why:
- F3: The 1-day-over-20-day volume ratio is graded the same way on the 72-bar grid. Its top quintile is followed by +0.0065 3-day excess (t 2.22) and its bottom quintile by −0.0058 (t −2.30). Its Spearman correlation with the excess is positive in all six coins (0.010 to 0.095, strongest in ZEC 0.095 and XRP 0.085). The top-minus-bottom spread holds in both halves of the 10-day scaled return (+0.0094 low half, +0.0151 high half).
- F4: Compression does not precede larger moves, against the brief. The narrowest 5-day high-low range quintile (scaled by 20-day volatility) is followed by a mean absolute 3-day move of 0.0549, about the same as the middle quintiles (0.052 to 0.056). The widest-range quintile is followed by 0.0663, and the highest 1-day-versus-20-day volatility quintile by 0.0619 against 0.0534 for the lowest. Large moves follow large moves, not quiet periods.
