---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline
line: 7.d not profitable
backtest: 029-02_breakout-volume-trapped-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close above the prior 20-day high is followed within 3 days by a close back below that high, the coin falls over the next 5 days, and the calmer the coin's last 20 days of daily moves against its last 60 days, the larger the fall.
Consequence: A trader would short failed breakouts in quiet markets and refuse them while volatility is expanding, when failures tend to rebound.
Why:
- F1: The book loses because after failed breakouts the coins rose. Over 385 first-in-cell short bets, the short's unusual 5-day move is -0.47 % (t -0.71) and its total move is -1.04 %, with a hit rate of 0.49. Step 5 finds -0.77 % unusual and -1.36 % total over 335 cases. The book is short (mean allocation -0.82) on 10.3 % of days, and on those days the coin gains +0.236 % a day while the book loses -0.203 % a day.
- F4: Turbulent conditions turn the failure into a rebound. The highest quartile of 20-day daily volatility loses -4.09 % (t -1.74, 79 cases), while the lowest gains +1.13 % (t 1.27). Rising volatility (20-day over 60-day volatility, top tercile) loses -2.44 % (t -1.64), and low 20-day return together with low volatility gives +1.00 % (t 1.20, 175 cases).
- F5: Cases already far below the broken high bounce. The deepest quartile, more than 10 % under the 20-day high, loses -3.32 % (t -1.42), against +0.46 % for the shallowest. The correlation of depth with the unusual move is +0.20, and 21.6 % of cases print a new 20-day high within 5 days.
