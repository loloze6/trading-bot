---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, with the rise building across the whole 3 days rather than in the first hours after the drop.
Consequence: Take the rebound once, when the drop is seen, and hold it for about 3 days rather than re-sizing it hour by hour, so the gain is not spent on fees.
Why:
- F1: The book loses to fees, not to the forecast. Before fees the positions summed to +1.80, but fees summed to 20.77 on a turnover of 19,205. Across 58,401 trades with a median hold of 5 hours, the mean trade made -0.386% before fees and -0.486% after. The book's mean daily return was -0.001116, against +0.00119 for holding the coins.
- F2: Most of the turnover is hourly churn, not new signals. Re-sizing inside a position made 10,712 of the 19,205 turnover (56%) and regime flips made 6,157 (32%). Forecasts switching on or off made only 2,336. Only 42% of active forecasts were still active 24 hours later.
- F3: The same forecast pays when held at its own horizon. Taking a position only at the 72-hour grid bars and holding it 72 hours gave a Sharpe of 0.48 after fees, with a daily mean of +0.000288 net and +0.000396 gross, against -1.44 for the hourly book.
