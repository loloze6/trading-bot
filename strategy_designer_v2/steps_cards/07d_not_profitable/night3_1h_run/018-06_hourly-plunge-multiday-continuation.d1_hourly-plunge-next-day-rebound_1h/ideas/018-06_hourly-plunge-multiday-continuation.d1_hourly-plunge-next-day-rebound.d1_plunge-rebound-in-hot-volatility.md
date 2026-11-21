---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's usual 1-day move, only while the coin's 3-day hourly volatility is high against its 30-day hourly volatility. The larger the drop in those multiples and the higher that volatility ratio, the larger the rise.
Consequence: A trader should buy a fresh plunge for a day only when it comes in an already agitated market, and refuse to buy the same plunge in a calm market, where it keeps falling.
Why:
- F1: The rebound sits almost entirely in the largest drops. After a drop of 3 or more multiples of the 30-day average absolute daily return, the next 24 hours end 0.38 of a usual 1-day move above the drift (+2.0 % raw, 376 cases). After drops of 1 to 3 multiples they end only 0.07 to 0.08 above (+0.46 % to +0.62 % raw, 2696 cases). The book traded all of them, so the idea's average unusual move is +0.11 % per case, 0.6 times the 0.19 % cost of a trade.
- F2: The rebound holds only when hourly volatility is already raised. Here that means the coin's 3-day hourly volatility is high against its 30-day volatility.
- F3: The book is long on 70 % of bars, and its daily returns correlate 0.71 with holding the coins. Bars whose 24-hour return was a rise still carried an average position of 0.17 (201,476 bars) and earned a summed gain of -0.13. The book is therefore mostly a diluted copy of holding the coins: its Sharpe is 0.02 below holding's.
- F4: The book's deepest fall is 52 %, spread over windows w14 to w21 (w17 121 days, w18 107, w16 54, w19 50). In these windows the book drifted while it held positions left over from mild, calm drops; holding's mean daily return there was mostly positive (for example w16 +0.45 % against the book's -0.11 %).
- F6: The rebound is done within a day. Hot drops of 3 or more multiples are +2.65 % above drift at 24 hours and +2.76 % at 72 hours, so a longer holding adds almost nothing.
