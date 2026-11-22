---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
line: 7.d not profitable
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 10-day high and within the next 3 days closes back just below that old high, the coin falls over the next 5 days, and the closer that close sits to the old high, the larger the fall.
Consequence: Short the many shallow 10-day breakout failures to trade often enough, and skip failures that have already fallen far below the old high.
Why:
- F1: The book barely trades and loses on the trades it takes: positions are open on 2.3 % of bars (0.007 trades per day), and its 126 trades average −1.19 % net (median −2.13 %, 29 % winners), although step 5's 70 cases show an unusual move of +1.75 % per 5 days.
- F3: The useful effect lies in how far below the old high the failure closes: shallow failures (close within 2.3 % below the old 20-day high) give +2.09 % (t 1.96, 64 cases), deep ones −1.03 % (t −0.80, 64 cases). The quartiles run monotonically from +2.19 % (shallowest) to −2.35 % (deepest), and the Spearman correlation of closeness with the move is 0.125.
- F7: A 10-day high nearly doubles the cases and keeps the shallow effect: 217 failures. Shallow 10-day failures give +1.58 % (t 1.77, 107 cases), deep ones −0.48 % (110 cases). Shallow and thin gives +3.28 % (t 1.93, 27 cases).
- F8: The edge is unevenly spread over time, which is why the book fails with one window left out. Shallow 10-day failures give +2.63 % (t 1.96, 55 cases) in w1–w12 and only +0.47 % (t 0.41, 52 cases) in w13–w24. The book's summed returns hinge on a few windows (w23 +6.9 %, w11 +4.5 %, w3 +4.1 %).
