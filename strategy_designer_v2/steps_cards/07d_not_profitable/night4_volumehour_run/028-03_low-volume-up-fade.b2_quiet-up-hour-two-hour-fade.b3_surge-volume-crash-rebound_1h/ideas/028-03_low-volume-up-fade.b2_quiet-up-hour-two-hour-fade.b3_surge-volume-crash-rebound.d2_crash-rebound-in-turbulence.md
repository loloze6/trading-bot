---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two hours. The rebound is larger the higher the coin's 30-day volatility stands against its 90-day average.
Consequence: A trader would buy heavy-volume hourly crashes when the market is already turbulent and refuse the same long in calm markets, where the bounce does not cover the cost.
Why:
- F1: The book loses on costs. Its gross gain per day (0.106 % BTC, 0.075 % ETH) is about half its fees per day (0.211 %, 0.182 %), on a turnover of 4.1 and 3.3 times the book per day. Its 25808 trades, median 2 hours, average +0.093 % before fees against a 0.11 % trade cost, so −0.007 % after fees. The mean daily book return is −0.112 % on both coins, while the coins themselves averaged +0.12 % and +0.14 % a day.
- F2: The idea is too small for the cost. Per case over 2 hours the total move is +0.04 % (0.4 times the 0.11 % cost) and the unusual move +0.03 % (strength 0.025, half that of the real ideas measured so far), over 14913 cases.
- F6: Among falls with a score above 10, the 2-hour rebound sits in high-volatility states: +0.27 % (t 1.30, 197 cases) when 30-day volatility is high against its 90-day average. In calm states it is +0.02 % (197) and in middle states −0.08 % (196). Only 58 % of windows have a positive mean.
