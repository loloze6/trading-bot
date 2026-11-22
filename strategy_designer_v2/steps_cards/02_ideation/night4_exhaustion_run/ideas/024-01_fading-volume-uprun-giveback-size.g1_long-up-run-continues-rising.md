---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen for many four-hour periods in a row, it keeps rising over the next three days. The longer the streak, and the larger its gain against the coin's typical four-hour move over the past 30 days, the larger the further rise.
Consequence: A long, strong up-run on 4h bars is a reason to be long or stay long for three days, not to short it.
Why:
- F1: Coins kept rising after up-runs instead of giving them back. On the first case per 18-bar cell, 4 or more 4h up bars in a row were followed over the next 3 days by a move above the coin's normal drift of +0.59 % (strength 0.069, t 2.58, n 1437) when volume faded. With rising volume the move was +0.51 % (strength 0.058, t 2.45, n 1813). The tested idea's short entries themselves showed +0.11 % (t 0.35, n 1258) against the short.
- F2: The continuation grew with the run. Runs of 6 or more up bars were followed by +1.38 % above drift over 3 days (strength 0.157, t 3.52, n 612). This is far above the 0.19 % cost of a trade.
- F3: Inside 4-bar up-runs the continuation also grew with the run's gain, measured in the coin's 30-day 4h volatility. By gain tercile the move over 3 days was −0.39 % (t −1.27, n 757) for the lowest, +0.66 % (t 2.34, n 756) for the middle and +1.03 % (t 2.25, n 757) for the highest.
- F6: The book lost on every coin, with mean daily returns from −0.033 % (BTC) to −0.080 % (ZEC) while holding the coins earned +0.07 % to +0.15 % a day. Its SHORT trades lost on average on every coin, from −1.15 % (BTC) to −4.37 % (ZEC) after fees, while its LONG trades gained +0.63 % to +2.57 %.
