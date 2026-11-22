---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The thinner a coin's weekend volume is relative to its own usual weekend-to-weekday volume ratio, the larger the share of its Saturday-Sunday 2-day return that is reversed over the next 2 days. A weekend of ordinary or heavy volume sees its move continued slightly.
Consequence: A trader leans against the weekend's move at Sunday's close in proportion to how unusually thin that weekend was for the coin, and stays aside or with the move when the weekend traded normally.
Why:
- F1: On Sunday's last bar, the coin's 48-hour weekend return is reversed over the next 48 hours only when the weekend's volume was thin against the coin's own usual weekend-to-weekday ratio. In the thinnest third of weekends (weekend/weekday volume 0.35 on average), the winsorised slope of the 48-hour future z on the past z is -0.27 (t -4.1, 636 cases). The middle third gives -0.07 (t -1.1) and the thickest third +0.07 (t 1.6).
- F2: The thinness grades the reversal continuously. In a regression of the Sunday 48-hour future z on the weekend move, log volume ratio and their product, the move's slope is -0.113 (t -3.1) and the product is +0.129 (t 4.7, about 1,900 cases). The thinner the weekend, the stronger the reversal.
- F3: The thin-weekend reversal is broad across coins and years. In the thin third, slopes are -0.32 to -0.48 for BTC, ETH, LTC and XRP (t -2.0 to -2.8), ZEC is -0.32 (t -1.4) and XMR is -0.01. Slopes are negative in 7 of 8 years (2023 is +0.13). Betting against the move gives +0.68 % above drift per case over 48 hours (t 2.7, 636 cases), which is 3.6 times the 0.19 % trade cost.
- F4: Moves of the same thinness made during the week are not reversed in the same way. In the thinnest third of each weekday, the 48-hour slopes are -0.01 to -0.10 (all |t| < 1.9), against -0.27 (t -4.1) on Sunday. This fits the brief's own discrimination test.
- F5: The tested forecast did not capture this. All Sunday cases pooled give a slope of -0.019 (t -0.6, 2,028 cases), and the tested forecast's unusual move was -0.29 % per case (t -0.19). Its form (move times the raw weekday/weekend ratio, standardised over 500 hourly bars) does not isolate the thin-weekend cases where the reversal sits.
