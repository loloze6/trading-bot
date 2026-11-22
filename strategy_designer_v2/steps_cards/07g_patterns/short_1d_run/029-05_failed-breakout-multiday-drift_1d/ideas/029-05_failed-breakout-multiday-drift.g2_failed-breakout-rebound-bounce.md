---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes back below its old 20-day high within 3 days of breaking above it, it rises over the next 8 days, and the larger the failure day's fall in units of its 20-day volatility, the larger that rise.
Consequence: A failed breakout that collapses hard is a reason to refuse a short and to expect a bounce.
Why:
- F3: The failures the book shorts are followed by rises, not falls. Over 8 days from the failure close the unusual move is +4.56 % (t 2.71, 131 cases); from 2 days later it is +3.80 % (t 1.90, 129 cases). The book's own cases average -0.36 % short-side (t -0.52), and its Sharpe is -0.40.
- F4: Inside the quintile of the largest down days relative to volatility, a failure adds to the rebound. Failures are followed by +7.43 % (t 2.61, 57 cases), against +1.96 % (t 2.16, 285 cases) for other days in that quintile.
- F5: Shallower failures rebound more than deeper ones, the reverse of the tested grading. The shallower depth half is followed by +6.10 % (t 2.27, 66 cases), the deeper half by +3.00 % (t 1.48, 65 cases).
