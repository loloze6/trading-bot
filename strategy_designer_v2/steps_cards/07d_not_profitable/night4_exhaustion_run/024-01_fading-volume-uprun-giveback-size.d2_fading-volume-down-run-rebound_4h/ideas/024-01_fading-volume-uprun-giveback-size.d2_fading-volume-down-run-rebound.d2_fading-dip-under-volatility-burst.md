---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise, the rise being larger the more the coin's 7-day volatility exceeds its 30-day volatility.
Consequence: A fading-volume sell-off in a calm market is a reason to refuse the rebound trade, and one in a market whose short-term swings have widened is a reason to take it.
Why:
- F2: The idea adds no move of its own. Its unusual 18-bar move is +0.00 % per case (t 0.002, 4537 cases), and the total move (+0.41 %) is only the coins' normal drift. The book holds a position on 78 % of bars at a mean allocation of about 0.68, so it is mostly a part-time long on the coins.
- F5: The rebound concentrates where 7-day volatility is high against 30-day volatility. In the top quintile of that ratio, cases rise +2.30 % above drift over 18 bars (t 1.98, n 102), against -0.43 % to +0.65 % in the other four quintiles. The book's bar gain there is +0.00097 (t 4.88), against -0.00003 to +0.00012 elsewhere.
