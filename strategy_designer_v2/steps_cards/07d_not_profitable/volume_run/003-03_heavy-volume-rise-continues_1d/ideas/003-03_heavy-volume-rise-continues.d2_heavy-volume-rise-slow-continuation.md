---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.d not profitable
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days. The further gain is spread over the days after the rise rather than concentrated in the next day, so the larger the rise and the heavier its volume, the larger the gain over the 2nd to 5th day after it, fading with the days since the rise.
Consequence: A trader would keep a heavy-volume rise's position for several days after it, sized down as the rise ages, instead of only for the day after it.
Why:
- F1: The book holds its position almost only on the signal day. Mean allocation is 0.53 on bars with a forecast above 0.5 and about 0.004 on each of the following 1 to 7 days. On the 511 signal grid bars the allocation is 0.76, but its mean over the next 5 bars is only 0.31. Mean absolute allocation per coin is 0.10 to 0.14.
- F2: The continuation the idea predicts comes after the first day, which the book does not hold. In the top forecast quartile (mean forecast 15.5, mean allocation 0.85), the next day's excess return is +0.00085 against +0.0091 summed over 5 days. Over all positive-forecast bars, the excess return is -0.00147 on day 1 (t -2.84, n 8742) and +0.00078, +0.00045, +0.00081 on days 2 to 4. On the 5-bar grid the excess return is +0.0169 (t 2.98, n 511).
- F3: The book therefore earns almost nothing. Its mean daily return is 4.9e-05 against 0.0012 for holding. The part it gets from the market's own rise is only 0.00007 to 0.00017 per coin. Fees take 1 to 5 % of the book per window, and the 2988 trades last 3.3 days on average with a 49 % win rate.
- F5: The continuation grows with the size of the rise and less clearly with its volume. By terciles of the scaled one-day rise it is 0.0118 (t 1.07), 0.0181 (t 1.88) and 0.0320 (t 3.08). By terciles of the volume ratio it is 0.0185, 0.0165 and 0.0269.
