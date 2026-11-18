---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls sharply over one day on volume well below its own 30-day average daily volume, it wins back part of that fall over the next 5 days, only while its 60-day return is positive. The larger the fall, the thinner its volume and the higher its 60-day return, the larger the rebound.
Consequence: A trader would buy thin-volume drops only in coins that have risen over the past 60 days, and would refuse them in coins in a downtrend.
Why:
- F3: The loss comes almost entirely from coins trading below their 50-day average. There, thin-volume down days lead to an excess 5-day return of −3.12 % (t −5.04, n 170). Above the average the same days give +0.06 % (t 0.07, n 134), and heavy-volume down days below the average give −0.94 % (t −0.73, n 92).
- F4: The coin's 60-day return grades this. For thin-volume down days, the excess 5-day return is −3.89 % in the lowest 60-day-return tercile (t −4.48, n 81), −2.92 % in the middle tercile (t −3.30, n 84) and +1.23 % in the top tercile (t 1.05, n 86).
- F5: On the book's own 5-day grid, active cases below the 50-day average lost −1.06 % excess (t −2.21, n 372), while those above it made +0.06 % (n 271). Every forecast quartile was negative (−1.10 % to −0.50 %), so the forecast's size does not grade the outcome.
