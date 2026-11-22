---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only for moderate Sunday moves: the opposite move grows with Sunday's 24-hour return up to about the coin's typical daily move and is smaller after Sunday moves much larger than that.
Consequence: A trader would fade typical Sunday moves fully and give the extreme ones a smaller bet, instead of the largest one.
Why:
- F4: The book sizes up exactly where the edge is weakest. The top quintile of |forecast| holds a mean position of 0.98 but gains only +0.13 % per case, below the 0.19 % cost. The middle quintiles hold 0.23–0.64 and gain +0.67 % to +0.87 %. Vol-scaling Sunday's move does not fix this: the volatility-scaled quintiles gain +0.16 % to +0.85 % with no rise at the top.
- F6: The failures show up in the falls and the daily gain. The book's daily chain falls by up to 31.0 % (worst in w13, w12, w9), giving a Calmar of 0.12, and its mean daily return is 0.014 %. Mondays (mean +0.108 %, standard deviation 1.78 %) and Tuesdays (+0.036 %, standard deviation 1.53 %) carry all of the risk. All 40 of the book's worst days fall on Monday (23) or Tuesday (17), so the falls come from the bets themselves, half of them the dead same-direction weekends.
