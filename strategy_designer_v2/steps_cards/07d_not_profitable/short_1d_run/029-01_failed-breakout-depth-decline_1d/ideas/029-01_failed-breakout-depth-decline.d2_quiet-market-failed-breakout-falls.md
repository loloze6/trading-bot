---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the coin's 20-day volatility of daily returns is low, and the lower that volatility, the larger the fall.
Consequence: A trader would short failed breakouts in quiet markets and refuse them in volatile, trending ones, where the book's deepest falls came.
Why:
- F1: The coin did not fall after a failed breakout: over 619 cases it rose, with a mean short-direction 5-day excess return of -0.48 % (t -1.18) and a total move of -1.06 %. The book's 1266 trades lost 2.75 % gross and 2.85 % net on average, with 28.9 % winners, so the loss is the signal's direction and not the 0.19 % cost of a trade.
- F3: The effect is also graded by the coin's 20-day volatility. In the lowest-volatility tercile the short excess is +0.54 % (t 1.10) and the total move is about 0 %. In the highest tercile it is -1.46 % (t -1.59) and the total move is -2.08 %. Low volatility together with low breakout volume gives +1.85 % (t 2.05, 68 cases), about ten times the cost of a trade.
- F6: The book's falls come from strong uptrends. Its worst windows are ZEC w24 (coin +1161 %, book -56 %), LTC w17 (coin +99 %, book -50 %) and ETH w17 (coin +55 %, book -38 %). Across windows the book's return correlates -0.40 with the coin's return. In 2020–2021 the book lost 0.149 % and 0.047 % a day while the coins gained about 0.42 % and 0.41 % a day.
