---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline
line: 7.d not profitable
backtest: 029-04_breakout-extension-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 20-day high, reaches further above it within the next 3 days, and then closes back below the old high, the coin falls over the next 5 days, only when the breakout day's volume was low against its 20-day average volume, and the lower that volume ratio was, the larger the fall.
Consequence: Short failed breakouts whose breakout day traded thinly, and refuse those whose breakout day traded heavily, because heavy-volume breakouts that slip back below the old high tend to recover.
Why:
- F5: Only breakouts made on thin volume failed into a decline. When the breakout day's volume was in the lowest quartile against its 20-day average (median 0.63×), the coin fell 1.45 % below drift over 5 days (t -1.91, 125 cases), about 7.6 times the cost of a trade. The higher-volume quartiles rose +1.50 %, -0.30 % and +1.78 % (slope of the move on volume ratio +0.0094, t 1.89, 500 cases).
- F1: Failed breakouts were followed by rises, not falls: over 605 cases, the 5-day move after the signal was +0.19 % above the coin's drift (t 0.44), and +0.77 % in total. A short therefore lost about four times the 0.19 % cost of a trade on average, and the book's mean daily return was -0.028 % (Sharpe -0.49, against a required mean of at least 0.05 %).
- F2: The grading runs against the idea: a larger peak excursion above the old high brought a larger 5-day rise (slope +0.0022 of return per percent of excursion, t 2.53, 605 cases). The top excursion quintile (median 10.3 %) rose +1.02 % above drift, against +0.03 % for the bottom quintile (median 1.4 %).
