---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin breaks above its 20-day closing high and within a few days closes back below it, the deeper that close sits below the old high, the more the coin rises over the next 2 days.
Consequence: A trader would refuse to short a failed breakout that has fallen deep below the old high, because the deeper failures bounce over the following days.
Why:
- F5: Contrary to the brief, the coin tends to rise after a close back below the old 20-day high within 5 days of a breakout. Its unusual 8-day move on the long side is +2.71 % over 196 cases, against -0.28 % on the other bars (Welch t 2.26). Most of this is the day-return reversal: with the scaled day return in the same regression, the failed-breakout term falls to +2.02 % (t 1.83) while the scaled return keeps t -4.24.
- F6: Among failed breakouts, the deeper the close below the old high, the larger the coin's rise over the next 2 days. The slope of the unusual move on the depth is -0.175 (t -3.61, 895 cases). Over 4 days it is -0.276 (t -2.36, 432 cases), which is the reverse of the tested idea's grading.
- F7: The book's daily returns are almost the mirror of the coin's moves. On the 4136 active coin-days their correlation is -0.86. The 30 best book days average +18.0 % on coin days of -17.1 %, and the 30 worst average -16.9 % on coin days of +15.1 %.
- F8: Trades lose money at every forecast size. The mean net result per trade is between -2.84 % and -3.48 % in all four quartiles of the entry forecast, and between -1.78 % and -4.29 % in every coin. A larger forecast brings no gain.
