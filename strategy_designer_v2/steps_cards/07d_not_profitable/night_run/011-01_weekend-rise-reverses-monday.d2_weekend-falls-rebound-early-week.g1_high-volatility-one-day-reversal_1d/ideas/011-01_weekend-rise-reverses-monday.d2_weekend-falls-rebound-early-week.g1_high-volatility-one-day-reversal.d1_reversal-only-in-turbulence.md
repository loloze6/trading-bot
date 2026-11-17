---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose last day's move was large relative to its 20-day volatility moves the opposite way over the next 1 day, and the reversal is larger the larger that scaled move and the higher the coin's 20-day volatility stands against its own history, only while its 20-day volatility stands well above its own 120-day average daily move.
Consequence: Fade violent days only in clearly turbulent stretches and stay out otherwise, so the book stops paying fees on calm-market fades that earn nothing.
Why:
- F1: Fees eat the gain: the position earns 0.000826 per bar before costs and pays 0.000706 per bar in fees on a turnover of 0.65 of the book per bar, so the book's daily mean is 0.000103 against holding's 0.001180.
- F2: The fade loses after costs in every volatility state except the most turbulent. Split by the coin's 20-day volatility against its 120-bar mean absolute move, the four lowest sextiles net -0.000706 to -0.001039 per bar (t -1.15 to -1.87, about 1480 bars each), the fifth nets 0.000429 (t 0.43), and only the top sextile (ratio 2.25) nets 0.003212 (t 3.49).
- F3: Even in calm sextiles the book carries mean |position| 0.30 to 0.46 and pays fees of 0.00050 to 0.00077 per bar, so the forecast's grading does not shrink exposure enough where there is no edge.
- F6: The result depends on the period. Inside the top two volatility sextiles net is negative in 9 of 23 windows (for example w12 -0.0065, w17 -0.0049, w21 -0.0040), and outside them it is negative in 16 of 24. This matches the failed leave-one-window-out Sharpe of -0.081 and the Calmar of -0.048.
