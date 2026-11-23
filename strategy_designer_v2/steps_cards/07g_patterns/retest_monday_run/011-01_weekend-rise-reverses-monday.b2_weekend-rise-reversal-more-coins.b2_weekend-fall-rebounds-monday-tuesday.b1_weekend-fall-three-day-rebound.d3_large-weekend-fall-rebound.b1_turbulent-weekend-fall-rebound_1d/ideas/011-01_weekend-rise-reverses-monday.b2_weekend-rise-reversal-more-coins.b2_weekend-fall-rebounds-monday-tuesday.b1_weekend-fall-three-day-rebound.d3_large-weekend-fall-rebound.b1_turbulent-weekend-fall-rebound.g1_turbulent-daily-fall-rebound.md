---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell on any day by a large multiple of its usual daily move rises over the next 3 days, more the deeper the fall and the higher its 20-day usual move stands against its 60-day usual move. In calm stretches, the same fall is followed by further decline.
Consequence: Buying sharp daily falls in turbulent stretches is not limited to Sunday, so the trader can apply it on every weekday and refuse falls that come in calm stretches.
Why:
- F1: On days other than Sunday, a coin's 3-day unusual move after a fall rises with the fall's depth (its daily return over its 20-day usual move) multiplied by its 20-day usual move against its 60-day mean. The slope is positive in 17 of 17 coins (per-coin t up to 3.2: DOGE 3.21, XMR 3.19, LTC 3.05), and the slope on date means is 0.0079 with t 2.26 over 1,234 dates; the tested Sunday-only idea does not account for this.
- F2: The same weekday falls (of at least 1.5 usual daily moves, Sundays excluded, t counted over dates) split by turbulence: those in the calmest third continue down by -1.15 % over 3 days (t -1.99, 368 cases on 163 dates), and those in the most turbulent third rebound by +1.09 % (t 1.79, 368 cases on 143 dates). The rebound is graded by turbulence and spread over Monday, Wednesday and Thursday (+1.46 %, +2.29 %, +1.51 %), not concentrated after the weekend.
