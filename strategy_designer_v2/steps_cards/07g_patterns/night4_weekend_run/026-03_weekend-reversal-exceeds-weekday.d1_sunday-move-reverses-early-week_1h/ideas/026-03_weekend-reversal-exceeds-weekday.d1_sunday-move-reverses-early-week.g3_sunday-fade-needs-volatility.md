---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's hourly volatility over the past 30 days, the larger the opposite move over Monday and Tuesday that follows each unit of its 24-hour return over Sunday.
Consequence: A trader would size the Sunday fade up in turbulent markets and leave it alone in calm ones, where the reversal is absent.
Why:
- F4: The tested Sunday reversal depends on volatility. Splitting each coin's Sunday cases into thirds by trailing 720-hour volatility, the slope of the 48-hour move on Sunday's scaled move is -0.13 (t -2.70, 671 cases) in the high-volatility third. It is -0.09 (t -1.84) in the middle third and +0.05 (t +0.78) in the low-volatility third. This is marginal given the many angles examined.
- F6: The book's daily returns are tied to the weekly cycle. Sunday's mean is -0.043 % (t -9.27, 2478 coin-days), which is the fee of entering at Sunday's last bar. Monday's mean is +0.108 % (t 2.10) and Tuesday's +0.036 % (t 0.80), so the gain sits in the first holding day.
