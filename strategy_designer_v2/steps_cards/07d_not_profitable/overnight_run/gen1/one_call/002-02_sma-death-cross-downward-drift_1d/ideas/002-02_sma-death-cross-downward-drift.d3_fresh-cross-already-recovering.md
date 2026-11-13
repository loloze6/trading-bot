---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, when the 50-day SMA has just crossed below the 200-day SMA and price closes back above its 50-day SMA, price rises over the next 10 bars by more than the coin's usual 10-bar move. A fresh cross with price already recovering marks a low that has passed, not the start of a downtrend.
Consequence: A trader would refuse shorts in a young death cross once price has reclaimed its 50-day average.
Why:
- F8: Shorting while price is already above its 50-day SMA and the spread is still widening loses -0.0416 per 10 bars in the mid-volatility tercile (n=253, t -4.54, overlapping).
- F9: Young death crosses lose and mature ones hold up better: shorts at most 60 bars into the state have a non-overlapping short gain of -0.0067 (n=398, t -1.05), against +0.0118 (n=212, t 1.27) for states older than 60 bars.
- F4: The book pays only when the whole market falls: it gains in 2018 (+2.62 summed daily gross, coin -0.0035 a day, 79% short) and 2022 (+0.93, coin -0.0018 a day, 89% short), and loses in 2020 (-5.35, coin +0.0042 a day) and 2024 (-2.96, coin +0.0024 a day), with window w16 alone at -4.66.
