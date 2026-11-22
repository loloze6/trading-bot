---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin whose 90-day return is positive, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is higher than the coin's normal 20-day drift, more so the larger the rise.
Consequence: A trader would treat a sharp one-day rise in a coin up over 90 days as a basis for a long over the next 20 days, larger the sharper the rise.
Why:
- F1: The short side carries the losses. Bars held short summed −2.44 in bar gains over 8081 bars, against +12.29 over 8577 bars held long. The 885 short trades lost 13.3 % net on average (median −8.1 %, 30.5 % winners), while the 675 long trades made +8.2 % (47 % winners).
- F4: The result rests on one window. In w17 the book made 3.5 % a day (Sharpe 2.61, short side +6.99). With w17 left out, the book's Sharpe falls to −0.058, against 0.45 to 0.57 when any other window is left out.
- F6: The tested gap itself is weak and unconfirmed. Up-regime minus down-regime is +2.17 % over 20 days, with Welch t 1.08 on 382 against 362 cases. The size is 0.048 of a usual move (+1.07 % total per case, 5.5 times the 0.19 % cost), so cost is not the cause. The cause is the short side's direction in recoveries.
