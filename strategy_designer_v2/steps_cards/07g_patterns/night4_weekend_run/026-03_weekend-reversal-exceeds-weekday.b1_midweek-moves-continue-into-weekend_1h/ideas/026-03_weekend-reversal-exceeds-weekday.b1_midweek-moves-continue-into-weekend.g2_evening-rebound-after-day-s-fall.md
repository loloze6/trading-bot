---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin is in a turbulent period (its 30-day hourly volatility high for it), its fall over the 20 hours up to the 19:00 UTC close is followed by a rise over the next two hours, 20:00 to 22:00 UTC. The larger that fall relative to its 30-day volatility, the larger the rise.
Consequence: A trader would buy a coin that has fallen through the day ahead of the 20:00-22:00 UTC rebound in turbulent periods, and would refuse to short it into those hours.
Why:
- F3: Hours 20:00 and 21:00 UTC carry the largest hourly drift of the day across the six coins: +0.055 % (t 6.75) and +0.044 % (t 5.66), about 17,400 cases each. That 2-hour return falls as the coin's return over the prior 20 hours rises (slope -0.000701 per standard deviation, t -5.85, 15,966 cases). After the lowest-quintile 20-hour moves it is +0.17 % (t 4.39); after the middle quintile it is about 0 (t -0.08).
- F4: The 20:00-21:00 UTC rise is concentrated in the high-volatility tercile: +0.136 % (t 4.90) there, against +0.014 % (t 1.00) and -0.000 % (t -0.02) in the lower two. The rise is positive in 6 of 8 years (2020 t 4.29, 2021 t 4.36, 2024 t 2.84) and negative in 2018 and 2023.
