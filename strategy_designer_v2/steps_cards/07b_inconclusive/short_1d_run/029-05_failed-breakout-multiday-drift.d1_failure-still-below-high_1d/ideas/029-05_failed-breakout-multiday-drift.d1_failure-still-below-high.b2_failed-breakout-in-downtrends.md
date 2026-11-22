---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.b inconclusive
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues while its close 2 days after the failure is still below that old high, only while the coin's 60-day return is negative. The further that day-2 close sits below the old high, the larger the fall over the next 16 days.
Consequence: A trader would short a failed breakout that stays below the old high only in a coin already falling over 60 days, hold it about two weeks and size it by the depth below the old high, and would refuse it in a coin rising over 60 days.
Why:
- F2: The effect only appears beyond a few days and grows with time: the mean unusual short move is -0.01 % at 2 days (t -0.05, 513 cases), +0.12 % at 4 days (t 0.29, 502), +1.05 % at 8 days (t 1.89, 486) and +2.12 % at 16 days (t 2.40, 445).
- F3: The effect sits in coins already falling over 60 days: with a negative 60-day return, cases move +1.70 % over 8 days (t 2.61, 320 cases) and +2.80 % over 16 days (t 2.99, 311). With a positive 60-day return they move -0.21 % (t -0.21, 166) and +0.52 % (t 0.26, 134).
- F6: The grading by depth holds only past the shallowest failures: the lowest depth tercile gives -0.49 % (t -0.50, 163 cases), the middle +1.96 % (t 2.24, 162) and the deepest +1.68 % (t 1.66, 161). The slope of the move on |forecast| is +0.0027 (t 1.69, 486 cases).
- F7: The market's own rise cancels the effect on the book: the coins' normal drift is -1.05 % per case in the short direction. That leaves a total move of -0.21 %, against a 0.19 % cost per trade. The total short move is about zero at every horizon (8 days: -0.004 %, t -0.01), and the book's Sharpe is -0.14.
