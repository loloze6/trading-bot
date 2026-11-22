---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 10 days, only while the coin's 20-day volatility of daily returns is low, and the lower that volatility, the larger the fall.
Consequence: A trader would short a failed breakout only in a calm coin and hold it for about two weeks rather than five days, scaling the short by how calm the coin has been.
Why:
- F2: The volatility condition sorts the cases the way the idea says, but the book is diluted by the volatile ones. Over 5 days, cases in the calmest quartile of 20-day volatility (below about 2.6 % a day) had an unusual move of +0.87 % (t 1.64, 155 cases). Cases in the most volatile quartile had -2.39 % (t -2.12, 155 cases): there, failed breakouts recovered.
- F3: The calm-market effect grows with the horizon. Over 10 days the calmest quartile had an unusual move of +1.84 % (t 1.83, 118 cases) and a total move of +0.73 %, against +0.87 % and +0.31 % over 5 days. The most volatile quartile went to -5.76 % (t -2.33, 118 cases).
- F4: Only the calm, longer-horizon version clears the cost of a trade (0.19 %) with room to spare. The calm 5-day total move of +0.31 % is about 1.6 times the cost, and the calm 10-day total move of +0.73 % is about 3.8 times. The 5-day total move over all cases (-0.69 % in the verdict) is negative.
- F5: The forecast does not grade the cases, so the book cannot lean on the calm ones through its signal.
- F7: Even the calm cases are not consistent across coins, so the calm-market effect is still fragile. Calm-quartile cases were positive in BTC (+1.82 %, t 2.38, 55 cases), XMR (+1.61 %, 36 cases) and ZEC (+2.65 %, 10 cases). They were negative in ETH, LTC and XRP.
