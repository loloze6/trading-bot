---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After a day in which the coin has moved far more than its usual daily move, measured as its 24-hour return over its 30-day hourly volatility scaled to a day, the coin moves back the opposite way over the next 24 hours. The larger that 24-hour move relative to its usual size, the larger the move back.
Consequence: A trader would lean against a coin's unusually large past day for the following day, and refuse to chase it.
Why:
- F1: Over 24 hours the coin moves against its own past day: across 5312 non-overlapping 24-hour cases, the rank correlation of the past 24-hour return (in units of its 30-day hourly volatility scaled to a day) with the next 24-hour drift-removed return is -0.079 (p 1e-8; slope -22.7 bp per unit). The effect holds on each coin (BTC -0.081, ETH -0.076), in w1-12 (-0.095) and in w13-24 (-0.067).
- F2: The 24-hour reversal is graded and is largest at the extremes. After the bottom quintile of past-day moves, the next day ends +31 bp (BTC) and +46 bp (ETH) above drift; after the top quintile, -21 bp and -16 bp. After past-day falls beyond 2 units it ends +146 bp (t 2.64, 133 cases). This spread is several times the 0.11 % cost of a trade.
- F3: The reversal does not reach 72 hours. The past 72-hour move against the next 72 hours gives a rank correlation of -0.006 (p 0.79, 1716 cases). The past 24-hour move against the next 72 hours gives -0.025 (p 0.30).
- F4: The tested situation shows no continuation; it leans toward a rebound instead. The 6-hour drift-removed return after hours falling more than 3 standard deviations is -10.8 bp in the idea's short direction terms, a rise of +10.8 bp (t 0.32, 177 cases). On volume above 4 times the average it is +27.6 bp (93 cases). The volume ratio's rank correlation with the outcome is 0.006 over 8416 cases.
