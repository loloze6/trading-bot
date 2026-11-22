---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, a one-day rise of several usual daily moves is followed over the next 5 days by a further rise when its 20-day return is positive, and the higher that 20-day return in usual daily moves, the larger the further rise.
Consequence: A trader would add to a sharp up-day the more the coin has already risen over the past 20 days, using a lookback short enough to be known on most bars.
Why:
- F2: The same rises in a coin whose 30-day return is positive keep going, and the larger the rise, the larger the follow-through. The unusual 5-day move is +2.77 % at 1 or more usual moves (t 3.27, 236 cases), +2.92 % at 1.5 or more (t 2.25, 123 cases) and +4.74 % at 2 or more (t 2.37, 62 cases). The 20-day return splits the rises the same way (+2.39 %, t 2.89, 245 cases).
- F4: The book trades too rarely because its situation is rarely knowable. Windows are only about 122 daily bars, so the 90-day return exists on just 26 % of bars and the regime fires on 236 of 17,524 bars. The book holds a position on 2.7 % to 5.6 % of bars per coin and makes 161 trades, or 0.0085 trades a day.
- F5: The book's gain is lost on the shorts. The 161 short trades average -3.06 % after fees (median -1.39 %), from +0.57 % on BTC to -7.27 % on XRP. The 15 trades held beyond 7 days average -27.6 % each, against -0.54 % for the 145 shorter ones. Daily book returns are negative in 13 of 24 windows (for example w18 -4.8 %, w20 -2.6 %), which leaves a mean daily return of 1.985e-05 and a Calmar of 0.055.
