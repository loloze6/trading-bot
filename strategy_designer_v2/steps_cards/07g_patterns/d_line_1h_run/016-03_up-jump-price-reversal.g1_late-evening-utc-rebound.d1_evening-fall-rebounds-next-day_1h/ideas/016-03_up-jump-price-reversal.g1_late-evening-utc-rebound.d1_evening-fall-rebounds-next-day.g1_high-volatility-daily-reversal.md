---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: On days when a coin's hourly moves have been large, the more it has fallen over the past 24 hours, the more it rises over the next 24 hours, and the more it has risen, the more it falls.
Consequence: After a violent day, a trader would hold a position against the day's move through the next full day, sized by the move's depth, and leave quiet days alone.
Why:
- F2: The 24-hour reversal sits almost entirely in high-volatility days. On the non-overlapping daily grid, the slope of the next-24h excess return on the past-24h return has t -8.91 in the top quintile of 24h summed absolute hourly moves (n 3422), against t between -0.50 and +1.24 in the other four quintiles. It is negative in all six coins on those days (t -2.15 to -4.92).
- F3: Inside that top-volatility quintile the response is graded and two-sided. The deepest-fall quintile (mean past return -11.8 %) gains a next-24h excess of +2.05 % (t 6.15, n 685). The quintiles above it fall steadily to -0.72 % (t -2.32, n 685) after the largest rises (+13.0 %).
- F1: The tested 20:00 position is held for one hour, not the 24 hours the idea measures, so the book cannot carry the rebound: its 7238 trades last 61 minutes on average, gross -0.095 % and net -0.195 % per trade (about 0.1 % fees each), and the 20:00→21:00 hour itself averages only +0.000051 (t 0.63), giving a book mean daily return of -0.000408 and Sharpe -2.24 over 2898 days.
