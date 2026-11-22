---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, and the smaller the breakout close's margin above that old high, the larger the fall.
Consequence: A trader would treat a marginal poke above the high that fails as a short, and a strong breakout that slips back as a likely second attempt higher.
Why:
- F1: The coin did not fall after a failed breakout: over 619 cases it rose, with a mean short-direction 5-day excess return of -0.48 % (t -1.18) and a total move of -1.06 %. The book's 1266 trades lost 2.75 % gross and 2.85 % net on average, with 28.9 % winners, so the loss is the signal's direction and not the 0.19 % cost of a trade.
- F4: The tested grading by depth below the old high does not appear: the depth terciles give -0.27 %, -0.65 % and -0.52 %. Breakout size grades the wrong way: breakouts under 0.7 % give +0.23 %, and breakouts over 2.4 % give -1.02 % (t -1.22).
- F5: 39.7 % of failed breakouts are followed within 5 days by a close above the breakout bar's close. Those 246 cases cost the short 7.2 %, while the other 373 cases earn 3.95 %. The brief's own refutation, a second successful break, is common, and it decides the result.
