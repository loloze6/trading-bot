---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin whose 3-day return is positive, the return over the next 4 hours from 05:00 UTC is negative, and the larger the 3-day rise against its recent range, the larger that morning decline.
Consequence: A trader would hold one longer morning fade of the 3-day rise each day, which captures a move that spans several hours with a single round trip of fees.
Why:
- F1: The book does not lose on its direction but on fees: its mean daily gain before fees is -0.000124 (t -1.02 over 2922 days), against 0.001699 a day in fees. That is about 1.8 round trips a day, each costing 0.0021 per unit of allocation, while the pre-settlement 2-hour excess return the book bets on averages only 0.000067 (t 0.37).
- F3: Of the three settlements, only 08:00 UTC shows the effect. On a 2-hour grid of up-trend cases, the 2-hour excess return falls with the standardised 72-hour rise in the window ending at 08:00 (slope -0.00134, t -4.05, top third minus bottom third -0.00227, n 2323). The window ending at 16:00 is flat (slope -0.000004, t -0.01, n 2385), and the window ending at 00:00 runs the other way (slope +0.00033, t 1.00, n 2367).
- F4: The 08:00 effect is not tied to the settlement itself. It belongs to a morning stretch: the slope of the 2-hour return on the rise is also negative for starts at 05:00 (t -2.07), 07:00 (t -3.26) and 08:00 UTC (t -1.99). Afternoon starts at 15:00 and 16:00 UTC have positive slopes (t +3.56 and +4.96), so after a 3-day rise the coin continues rather than reverses in the afternoon.
