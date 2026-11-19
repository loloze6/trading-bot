---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run up, the return over the 2 hours before the 08:00 UTC funding settlement is negative, and the stronger the 3-day rise, the larger that pre-settlement decline, only at the 08:00 UTC settlement and not at 00:00 or 16:00.
Consequence: A trader would fade a 3-day rise only into the 08:00 UTC settlement, which cuts two thirds of the fee-paying round trips that earn nothing.
Why:
- F1: The book does not lose on its direction but on fees: its mean daily gain before fees is -0.000124 (t -1.02 over 2922 days), against 0.001699 a day in fees. That is about 1.8 round trips a day, each costing 0.0021 per unit of allocation, while the pre-settlement 2-hour excess return the book bets on averages only 0.000067 (t 0.37).
- F3: Of the three settlements, only 08:00 UTC shows the effect. On a 2-hour grid of up-trend cases, the 2-hour excess return falls with the standardised 72-hour rise in the window ending at 08:00 (slope -0.00134, t -4.05, top third minus bottom third -0.00227, n 2323). The window ending at 16:00 is flat (slope -0.000004, t -0.01, n 2385), and the window ending at 00:00 runs the other way (slope +0.00033, t 1.00, n 2367).
- F5: The size of the one working window barely covers the costs. Its top-third-minus-bottom-third spread of -0.00227 is about one round-trip fee (0.0021). Down-trend episodes show nothing either: 2-hour excess return 0.000078, t 0.41, n 7137.
