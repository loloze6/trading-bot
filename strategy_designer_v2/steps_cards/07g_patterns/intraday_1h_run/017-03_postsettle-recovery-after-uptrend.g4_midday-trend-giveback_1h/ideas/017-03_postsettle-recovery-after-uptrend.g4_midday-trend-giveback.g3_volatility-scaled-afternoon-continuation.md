---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 3 hours from 15:00 UTC, a coin moves in the direction of its own 3-day return, and the larger its 1-day volatility, the larger that move in the direction of its 3-day return.
Consequence: In volatile conditions, afternoon trend-following has a larger expected move per trade, which matters when costs are as heavy as they were here.
Why:
- F1: In the hours from 15:00 UTC a coin carries on with its 3-day trend instead of reversing it. One case per day per coin, about 16,860 cases per hour, regressed on the minus-3-day-return signal: the bar stamped 14:00 gives a slope of -7.6 bp (t -6.0), the bar stamped 15:00 gives -10.5 bp (t -8.9) and the bar stamped 16:00 gives -4.7 bp (t -4.1). At the 14:00 bar, the strongest-uptrend fifth then gains +13.7 bp over 3 hours and the strongest-downtrend fifth loses -14.6 bp.
- F2: This afternoon continuation is broad but fading. At the 14:00 bar the slope is negative in all six coins, with t between -2.7 and -4.0 in BTC, ETH, LTC and ZEC. It is significant in every year from 2018 to 2021 (t -2.4 to -5.3) but not in 2022 to 2025 (t +1.6 to -1.0). It grows with the past 24-hour volatility tercile: -4.8, -7.2 and -10.1 bp, with t -2.8, -3.8 and -3.7.
- F5: The book is eaten by trading costs. Over all windows, the sum of position times next-bar return is 4.9, while fees come to about 20.3 measured the same way. With about 1.5 trades per day, that explains a Sharpe of -2.73 despite a confirmed signal (t 4.38).
