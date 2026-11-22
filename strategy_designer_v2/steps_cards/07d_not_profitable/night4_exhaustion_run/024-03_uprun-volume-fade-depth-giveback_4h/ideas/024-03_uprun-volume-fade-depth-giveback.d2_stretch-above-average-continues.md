---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The further a coin's price stands above its average price of the past 30 days, the more it rises over the next three days.
Consequence: If confirmed, being above the 30-day average is a reason to refuse shorts against up-runs and to hold the coin long.
Why:
- F2: Most of the book's loss is the coins' own rise paid by a standing short: of the -0.192 % mean daily return, -0.139 % is the market part (position × the coins' mean daily return) and only -0.052 % is timing. This is what drags Sharpe (-0.83), the mean daily return and Calmar (-0.65) below their rules.
- F4: The give-back is concentrated in mid-sized runs and reverses in the largest ones.
- F5: The give-back appears only when the coin is not already far above its 30-day level.
