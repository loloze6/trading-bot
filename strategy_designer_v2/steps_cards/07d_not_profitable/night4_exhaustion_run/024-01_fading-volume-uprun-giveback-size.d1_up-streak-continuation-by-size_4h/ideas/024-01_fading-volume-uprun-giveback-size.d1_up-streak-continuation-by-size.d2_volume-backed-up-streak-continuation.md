---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods while the volume of its bars grows from one period to the next, it keeps rising over the next three days, and the faster the volume grows during the streak, the larger the further rise.
Consequence: An up-run carried by growing volume is a reason to join it for three days, and one on shrinking volume is a reason to stay out.
Why:
- F2: The book is mostly long the coin's drift and adds no timing. Per case, the unusual move is -0.09 % (strength -0.009, 5723 cases) against a cost of 0.19 % a trade. The total move of +0.32 % is almost all normal drift (+0.41 %). Book and coin daily means move together by year, for example 2018 at -0.30 % against -0.35 % and 2022 at -0.21 % against -0.19 %.
- F6: Volume points weakly against the brief's fading-volume story. Streaks where volume rose bar by bar (top tercile of the volume slope) were followed by +0.58 % excess, against -0.21 % and -0.19 % for falling or flat volume (about 341 cases each). Inside rising 30-day trends, low-volume streaks did +0.42 % (t 1.13, n 510) and high-volume ones +0.18 % (t 0.49, n 632). Neither split is statistically reliable.
