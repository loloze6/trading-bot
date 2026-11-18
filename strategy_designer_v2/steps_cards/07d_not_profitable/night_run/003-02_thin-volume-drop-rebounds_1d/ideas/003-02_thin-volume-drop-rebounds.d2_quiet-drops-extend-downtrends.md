---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin whose 60-day return is negative falls over one day on volume below its own 30-day average daily volume, it keeps falling over the next 5 days. The further its 60-day return is below zero, the larger the further fall.
Consequence: A trader would treat a quiet down day in a falling coin as a sign that the decline continues, either to short it or to stay out of longs.
Why:
- F2: Thin-volume down days give no rebound; they keep falling. On the 10-day grid they show an excess return of −0.70 % over 2 days (t −2.27, n 395) and −0.89 % over 5 days (t −1.84). Up days show +0.54 % over 5 days (t 1.26).
- F3: The loss comes almost entirely from coins trading below their 50-day average. There, thin-volume down days lead to an excess 5-day return of −3.12 % (t −5.04, n 170). Above the average the same days give +0.06 % (t 0.07, n 134), and heavy-volume down days below the average give −0.94 % (t −0.73, n 92).
- F4: The coin's 60-day return grades this. For thin-volume down days, the excess 5-day return is −3.89 % in the lowest 60-day-return tercile (t −4.48, n 81), −2.92 % in the middle tercile (t −3.30, n 84) and +1.23 % in the top tercile (t 1.05, n 86).
