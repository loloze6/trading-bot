---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.b inconclusive
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall.
Consequence: Weekend rallies are partly given back once weekday liquidity returns, which is a reason to refuse chasing them on Monday or to lean short against them.
Why:
- F5: The opposite side shows more clearly. Sunday rises are followed by a mean excess 2-day return of -0.0098 (t -4.26, n 1083). Across all Sundays, the slope of excess 2-day return on the Sunday move in usual moves is -0.0046 (t -2.46). No other weekday has a 2-day slope with |t| above 1.6.
- F2: The plain rebound exists but is weakly graded. Sunday drops are followed by a mean excess 2-day return of +0.0065 (t 2.84, n 967), against +0.00044 after weekday drops (Welch t, Sunday minus weekday, 2.46). Yet the deepest quartile of drops rebounds less (+0.0047, t 0.90) than the second and third quartiles (+0.0113 and +0.0101, t 2.64 and 2.20). The depth-weighted product therefore reaches only t 1.53, and the grading the plan rewards is what dilutes it.
