---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, and grows more the higher the coin's 7-day volatility stands against its 60-day volatility, and it is gone by the second day after settlement.
Consequence: A trader sizes the settlement-fall long up when recent volatility is high against its usual level and leaves shallow falls in calm markets alone, where the move does not cover the cost.
Why:
- F4: The information lies in the deeper falls. The two lowest of the five forecast quintiles gave −0.08 % and −0.16 % unusual 24-hour moves (t −0.71, −1.36), against +0.41 % (t 3.23) and +0.19 % (t 1.39) in the two highest, around 1700 cases each. The deepest two quintiles in a rising 30-day trend gave +0.47 % unusual (t 3.41, 1241 cases) and +0.61 % total, 3.2 times the cost, against −0.05 % (t −0.32, 1333 cases) in a falling trend.
- F5: The recovery is larger when the coin's recent volatility is high. In the top third of the 7-day against 60-day volatility ratio, signal cases gave +0.26 % unusual (t 2.54, 2876 cases) and +0.42 % total. The same third without a signal gave −0.22 % (t −2.24, 2854 cases), so the condition alone does not earn. The lower two thirds gave −0.05 % and −0.01 % with a signal.
- F6: Trades last 34 to 54 hours on average, well beyond the 24-hour horizon. Net gains per trade are only +0.02 % to +0.09 % in the middle forecast quintiles, against +0.32 % to +0.35 % at the extremes, so the book's holding and middle-strength entries add exposure without adding effect.
