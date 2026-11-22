---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, a one-day rise of several usual daily moves is followed over the next 5 days by a further rise when its 30-day return is positive, and the larger the rise in usual daily moves, the larger that further rise.
Consequence: A trader would buy sharp up-days in coins up over the last month, larger the sharper the day, instead of fading bounces, which carry no edge in falling coins.
Why:
- F2: The same rises in a coin whose 30-day return is positive keep going, and the larger the rise, the larger the follow-through. The unusual 5-day move is +2.77 % at 1 or more usual moves (t 3.27, 236 cases), +2.92 % at 1.5 or more (t 2.25, 123 cases) and +4.74 % at 2 or more (t 2.37, 62 cases). The 20-day return splits the rises the same way (+2.39 %, t 2.89, 245 cases).
- F1: The fade the book bets on is not in the bars. On the non-overlapping 5-day grid, a one-day rise of at least 1 usual daily move while the 30-day return is negative is followed by an unusual 5-day move of +0.29 % (t 0.33, 116 cases). At 2 or more usual daily moves it is -1.43 % (t -0.83, 30 cases). Neither is distinguishable from zero.
- F4: The book trades too rarely because its situation is rarely knowable. Windows are only about 122 daily bars, so the 90-day return exists on just 26 % of bars and the regime fires on 236 of 17,524 bars. The book holds a position on 2.7 % to 5.6 % of bars per coin and makes 161 trades, or 0.0085 trades a day.
- F6: The cost is not what blocks the book. Per trade the gap between gross and net is about 0.10 %, small next to the 5-day usual move of 7.9 % to 13.9 %. The loss comes from the direction of the bet: shorting rises that F1 shows do not fade, in coins whose rises (F2) tend to continue.
