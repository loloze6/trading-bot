---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline
line: 7.c rejected
backtest: 029-04_breakout-extension-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its highest close of the prior 20 days, it rises more than its normal drift over the next 10 days, and the further the close clears that old high, measured in units of the coin's 20-day daily volatility, the larger the rise.
Consequence: A daily close through the 20-day high is a reason to be long for about ten days rather than to wait for the break to fail, with more conviction the larger the break relative to the coin's volatility.
Why:
- F5: Plain closes above the prior 20-day closing high were followed by rises well above the coin's drift. The unusual move was +0.93 % at 3 days (t 3.4, 1018 cases), +1.34 % at 5 days (t 3.1, 799 cases) and +2.99 % at 10 days (t 3.6, 558 cases). The 10-day total move was +4.2 %, about 22 times the 0.19 % cost of a trade.
- F6: Those breakout rises grew with how far the close cleared the old high, measured in units of the coin's 20-day daily volatility. At 5 days the quintiles went from +0.23 % (lowest) to +2.1 % and +2.2 % (top two, t 2.4 and 2.0, about 160 cases each). The linear slope was t 1.9 at 5 days and t 2.5 at 10 days, but ranks are weaker (Spearman 0.04–0.05, p about 0.28).
- F3: Failed breakouts were followed on average by a small rise, not a fall. The long-signed unusual move was +0.19 % at 5 days (t 0.52, 751 cases) and +0.94 % at 10 days (t 1.29, 578 cases). This was not stable across years: 2019 was −2.8 % (t −2.7, 83 cases) and 2020 was +2.5 % (t 3.2, 117 cases).
