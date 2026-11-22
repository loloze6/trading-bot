---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise is followed by a fall over the next day, and the larger that rise against the coin's 20-day standard deviation of daily returns, the larger the next day's fall.
Consequence: A trader would fade sharp bounces in falling coins for one day only, and refuse to hold the fade for several days or to fade bounces in coins rising over 90 days.
Why:
- F1: In coins whose 90-day return is negative, the next day's return falls steadily as the day's rise grows against its 20-day standard deviation. After a rise of 0.5 to 1 usual moves the next day averages +0.08 % (n 306, t 0.28). After 1 to 2 usual moves it averages −0.64 % (n 191, t −1.89). After more than 2 it averages −1.36 % (n 65, t −2.16). In coins whose 90-day return is positive, the same rises are followed by gains: +0.27 % (n 250, t 0.80) and +0.42 % (n 76, t 0.56).
- F2: The fade does not last to the tested 5-day horizon. On the non-overlapping 5-day grid, rises of more than 2 usual moves in falling coins are followed by an unusual move of +0.058 usual 5-day moves (n 17, t 0.32), which is upward, not a fall. In the backtest, the 1045 short cases gave back only 0.026 of a usual move (t 0.78) against a cost of 0.19 % per trade. So the short held 5 days keeps the one-day giveback of F1 and then carries 4 more days of noise.
