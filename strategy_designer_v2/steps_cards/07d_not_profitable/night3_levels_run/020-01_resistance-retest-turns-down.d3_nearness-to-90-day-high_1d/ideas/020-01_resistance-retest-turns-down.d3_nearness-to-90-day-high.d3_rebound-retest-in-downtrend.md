---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's 90-day highest close has been falling over the past 20 days, the further the close has rebounded from its low back toward that falling high, the more the coin falls over the next 5 days.
Consequence: In a falling coin, a trader should read a partial rebound toward the old high as a reason to refuse a long, and possibly to go short.
Why:
- F2: The book loses inside its falling legs and earns everywhere else. Those legs cover 1450 of 2898 days, where its daily returns sum to -1.85 (holding: -3.37); on the other days they sum to +4.46.
- F3: Inside the falling legs, nearness to the 90-day high is followed by falls instead of rises. The nearest quintile, held at a position of 1.05, loses 0.32 % per bar, and its 5-day return is -1.27 % (t -2.32, 253 cases); middle nearness is also followed by falls, -1.11 % to -1.79 % (t -2.4 to -3.1). Outside the legs, the nearest quintile is followed by +3.98 % (t 5.51, 449 cases).
- F4: In the bear years 2018 and 2022, closes at middle nearness are followed by the largest falls: quintile 2 by -3.82 % over 5 days (t -4.53, 119 cases), quintile 3 by -3.45 % (t -2.37, 57). The book still holds them at positions of 0.58 and 0.62, against 0.37 and 0.53 over all years. Its forecast is standardised against nearness's own last 90 values, so a partial rebound in a falling market reads as "near".
