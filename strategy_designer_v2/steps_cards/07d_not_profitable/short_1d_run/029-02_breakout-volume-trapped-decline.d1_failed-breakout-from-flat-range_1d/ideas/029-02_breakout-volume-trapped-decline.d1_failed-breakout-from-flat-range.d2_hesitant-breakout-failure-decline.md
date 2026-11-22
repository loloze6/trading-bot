---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
line: 7.d not profitable
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close above the prior 20-day high is followed within 3 days by a close back below that high, the coin falls over the next 5 days, and the smaller the breakout close's excess above the old high, the larger the fall.
Consequence: A trader would short failures of hesitant breakouts that barely cleared the high and refuse failures of forceful, high-volume breakouts, which tend to resume upward.
Why:
- F1: The idea's effect is not in the data. On my own non-overlapping recount of failed breakouts, the unusual short-direction move over 5 days is -0.26 % per case (t -0.36, 245 cases), and step 5 measured -0.36 % (t -0.85, 641 cases). Failed breakouts are therefore followed by slightly more rise than the coin's normal drift, not by a fall.
- F7: Forceful breakouts recover rather than fail.
- F8: The tested grading by the pre-breakout run-up does not hold. By quartile of the 20-day pre-breakout return, the unusual move is -0.79 %, -0.34 %, +0.22 % and -0.13 %, with no ordering. Step 5's slope t is -1.49.
