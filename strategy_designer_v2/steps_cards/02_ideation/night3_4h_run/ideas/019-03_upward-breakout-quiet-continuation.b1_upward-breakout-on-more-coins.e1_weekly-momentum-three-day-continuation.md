---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's return over the past 7 days, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift.
Consequence: A trader should lean long a coin over the next three days in proportion to how strongly it rose over the past week, and away from coins that fell.
Why:
- F4: The coin's past 7-day return grades the 18-bar move after breakouts. By quintile of the 7-day return over the 30-day volatility, the unusual move runs from −1.03 % (strength −0.10, t −4.38) to −0.46 %, +0.50 %, +0.51 % and +1.12 % (strength +0.098, t 2.19), about 1000 cases each. The plain 7-day return gives the same order, from −1.16 % (t −4.71) to +1.23 % (t 2.33).
- F5: The same past-week grading holds on ordinary bars, so it is momentum rather than a breakout effect. On all 18-bar grid bars (about 1821 cases per quintile), the unusual move by quintile of the 7-day return over volatility is −0.18 %, −0.71 % (t −3.87), −0.47 % (t −2.28), +0.22 % and +0.92 % (t 3.18, strength 0.094). The 30-day return grades breakout cases the same way, from −0.41 % and −0.60 % (t −2.40) in the two lowest quintiles to +0.78 % (t 2.59) and +0.93 % in the two highest.
- F6: The book earns in coins that rose the week before. Its mean daily return by quintile of the coin's prior 7-day return goes from −0.039 % to −0.011 %, +0.044 %, +0.134 % and +0.370 %, while its mean allocation goes from 0.16 to 0.71. Trades entered in the highest 7-day quintile net +3.82 % on average, against +0.46 % in the lowest (about 1984 trades each).
- F1: Most of the book's gain is the market's own rise, not timing: the book's mean daily return is 0.1003 %, of which 0.0709 % is the position held times the coins' mean daily return and only 0.0293 % is timing, over 2898 days. Holding the coins earns more per day (0.1388 %); the book's higher Sharpe (0.92 against 0.61) comes from being invested only about 55 % of the bars.
