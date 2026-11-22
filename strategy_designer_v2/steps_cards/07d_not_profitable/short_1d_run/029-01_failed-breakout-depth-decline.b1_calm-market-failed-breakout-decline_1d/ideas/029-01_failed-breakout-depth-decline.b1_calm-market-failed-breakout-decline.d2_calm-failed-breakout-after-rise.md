---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 10 days, only while the coin's 20-day volatility of daily returns is low and its 60-day return is positive, and the lower that volatility, the larger the fall.
Consequence: A trader would refuse to short a failed breakout that comes after a long decline, where it tends to mark a rebound, and short it in a calm coin that has been rising.
Why:
- F2: The volatility condition sorts the cases the way the idea says, but the book is diluted by the volatile ones. Over 5 days, cases in the calmest quartile of 20-day volatility (below about 2.6 % a day) had an unusual move of +0.87 % (t 1.64, 155 cases). Cases in the most volatile quartile had -2.39 % (t -2.12, 155 cases): there, failed breakouts recovered.
- F3: The calm-market effect grows with the horizon. Over 10 days the calmest quartile had an unusual move of +1.84 % (t 1.83, 118 cases) and a total move of +0.73 %, against +0.87 % and +0.31 % over 5 days. The most volatile quartile went to -5.76 % (t -2.33, 118 cases).
- F6: The losses cluster in volatile, rebounding stretches.
