---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 10-day average volume relative to its own 60-day average volume, the more its price rises over the next 3 days relative to its usual 3-day return.
Consequence: Rising participation is a reason to lean long for the next few days, and fading volume is a reason to refuse or cut a long.
Why:
- F1: Recent volume predicts the next 3 days' excess return across its whole range, even after allowing for the tested advance. On the 3-day grid, the bars in the top quintile of 10-day mean volume over 60-day mean volume returned +0.0104 above the coin's usual 3-day return (t 2.94, n 857). The bottom quintile returned −0.0072 (t −2.63, n 857). In a regression of excess return on both log volume ratio and the volatility-scaled 10-day return, the volume ratio's beta is 0.0140 (t 4.61), against the scaled return's t of 2.13. The Spearman correlation is 0.045 (p 0.003).
- F2: The volume pattern holds in every coin. The top volume quintile's excess is positive in all six coins, from +0.0032 (BTC, n 115) to +0.0188 (XRP, n 153). The bottom quintile's excess is negative in all six, from −0.0008 (BTC) to −0.0127 (ETH, t −2.36). The top quintile is positive in 6 of 8 years, with 2024 at +0.0322 (t 4.03, n 135) and 2020 at +0.0209 (t 2.27).
- F3: The pattern also holds on a 3-day volume ratio and partly on a 10-day horizon. A 3-day volume surge (3-day mean over 60-day mean, top quintile) is followed by +0.0100 excess over 3 days (t 2.83, n 857), against −0.0052 for the bottom quintile (t −1.90). At a 10-day horizon the top volume quintile gives +0.0174 excess (t 1.51, n 252), which is the same sign but weak.
