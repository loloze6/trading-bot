---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 2-hour return into the US market open, read at a bar closing between 12:00 and 14:00 UTC, the more of it the coin gives back over the next 2 hours.
Consequence: A trader fades sharp moves into the US open for the next two hours, and refuses to follow them.
Why:
- F6: The 2-hour reversal is strongest at the US open. For bars closing at 12:00–14:00 UTC, the top quintile of |2h move| is followed by a contrarian 2-hour return of +0.271 % (t 7.2, 3915 cases), against +0.061 % (t 5.9) at the other hours. Within those hours it grows from −0.009 % in the second quintile to +0.090 % (t 3.6) in the fourth and +0.271 % in the fifth.
- F1: The 2-hour reversal is not tied to funding settlement. Measured on every bar, the drift-removed contrarian 2-hour return after a 2-hour move is +0.062 % (t 4.9) for bars closing at 00:00 UTC, +0.009 % (t 0.8) at 08:00 and +0.042 % (t 3.4) at 16:00. Non-settlement closes are as large or larger: +0.082 % (t 6.6) at 12:00, +0.072 % (t 6.5) at 21:00 and +0.071 % (t 6.2) at 01:00. This is the brief's third way of being wrong.
