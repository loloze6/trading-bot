---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The further that day-2 close sits below the old high, the larger the fall from day 2 to day 10.
Consequence: A trader would short a failed breakout only once price has stayed below the old high for two days, sized by the current distance below it, and would refuse the short when price is already back above.
Why:
- F3: The tested grading runs backwards. Failures in the shallowest third of depth (mean 0.54 % below the old high) are followed by a rise from day 2 to day 10, with an unusual move of -2.91 % (t -3.03, 157 cases). The deepest third (5.7 % below) is flat over that span (+0.23 %, t 0.20) but rises over days 0 to 2 (-1.18 %, t -2.45).
- F4: Which way the drift runs is decided by where price stands at day 2. When the coin is already back above the old high at day 2 (31.5 % of failures), it keeps rising over days 2 to 10, with an unusual move of -4.27 % (t -2.37, 148 cases); that is the second, successful break the brief names as its refutation. When it is still below the old high, days 2 to 10 give +0.76 % (t 1.20, 322 cases).
- F2: While the book is short (27.0 % of bars, mean position -0.97), the coin's next-bar return is +0.153 %, against +0.119 % on all bars, so each short bar loses 0.090 %. The book is short just before the coin rises more than usual.
