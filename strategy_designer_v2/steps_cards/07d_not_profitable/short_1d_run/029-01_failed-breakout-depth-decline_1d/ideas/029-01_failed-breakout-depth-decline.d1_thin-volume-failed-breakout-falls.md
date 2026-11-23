---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the breakout day's volume was below its 20-day average, and the lower that volume against its average, the larger the fall.
Consequence: A trader would short only failed breakouts that came on thin volume, and stand aside from those that came on heavy volume, which tend to break higher again.
Why:
- F1: The coin did not fall after a failed breakout: over 619 cases it rose, with a mean short-direction 5-day excess return of -0.48 % (t -1.18) and a total move of -1.06 %. The book's 1266 trades lost 2.75 % gross and 2.85 % net on average, with 28.9 % winners, so the loss is the signal's direction and not the 0.19 % cost of a trade.
- F2: The effect is graded by the breakout day's volume against its 20-day average, but it only points the right way at the low end. In the lowest volume tercile the short excess is +0.72 % (t 1.14, strength +0.079, 206 cases). In the middle tercile it is -0.87 % and in the highest -1.29 % (t -1.59, strength -0.108), with a Spearman correlation of -0.062 between volume ratio and short excess.
- F3: The effect is also graded by the coin's 20-day volatility. In the lowest-volatility tercile the short excess is +0.54 % (t 1.10) and the total move is about 0 %. In the highest tercile it is -1.46 % (t -1.59) and the total move is -2.08 %. Low volatility together with low breakout volume gives +1.85 % (t 2.05, 68 cases), about ten times the cost of a trade.
- F5: 39.7 % of failed breakouts are followed within 5 days by a close above the breakout bar's close. Those 246 cases cost the short 7.2 %, while the other 373 cases earn 3.95 %. The brief's own refutation, a second successful break, is common, and it decides the result.
