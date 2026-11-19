---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days, with the follow-through growing more than in proportion to the week's rise, so that it is concentrated after the largest weekly rises and almost absent after small ones.
Consequence: In a rising month, a trader should commit size only after a coin's strongest weeks, and not pay fees to hold small positions after modest weekly gains that carry no follow-through.
Why:
- F1: The book's gain is mostly eaten by fees. Gross gain averages 3.6e-05 per hour against 1.6e-05 of fees, so fees take about 45% of it, and this is what leaves the mean daily return at 0.00045, below the 0.0005 bar.
- F2: The loss sits in the weak forecasts. Bars with a forecast between 0 and 2 net -3.1e-05 per hour and bars between 2 and 5 net -3.2e-05, because their fees (2.1e-05 and 4.1e-05) exceed their gross gain (-1.0e-05 and 8.4e-06). Bars between 10 and 20 net +1.41e-04 per hour on a mean position of 0.84.
- F3: The follow-through is not proportional to the week's rise. On the trending 168-bar grid, the two lower 7-day-return quartiles return -0.011 to +0.017 (t between -1.06 and 1.25). The two upper quartiles return 0.024 to 0.039 (t 1.86 to 2.23). On the 24-hour grid, long bars in the two lowest 7-day quintiles earn 0.00003 and -0.00005 (t about 0.6), against 0.0029 to 0.0037 (t 3.5 to 4.0) in the top two.
- F4: The forecast level shows the same shape. On the 24-hour grid, long bars in the top forecast quintile (mean forecast 18.7) earn 0.0057 per day (t 4.8), while the quintile with mean forecast 4.3 earns 0.0006 (t 2.7) and the two lowest quintiles earn about 0.
