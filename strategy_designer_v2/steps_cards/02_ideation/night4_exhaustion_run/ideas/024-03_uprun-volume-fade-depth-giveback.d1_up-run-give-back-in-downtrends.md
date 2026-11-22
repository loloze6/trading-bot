---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of rising four-hour periods whose gain is large relative to the coin's typical four-hour move over the past 30 days, the coin falls over the next three days, the larger the streak's gain the larger the fall, only while the coin's price is below its average price of the past 30 days (the further below, the larger the fall).
Consequence: A trader would short up-runs only as relief rallies inside a coin's 30-day downtrend, and refuse to short runs made while the coin trades above its 30-day average, where shorts pay the coin's rise.
Why:
- F2: Most of the book's loss is the coins' own rise paid by a standing short: of the -0.192 % mean daily return, -0.139 % is the market part (position × the coins' mean daily return) and only -0.052 % is timing. This is what drags Sharpe (-0.83), the mean daily return and Calmar (-0.65) below their rules.
- F3: Per case, the give-back is smaller than a trade's cost: the unusual 18-bar fall is +0.13 % (strength 0.014, t 1.15, 5709 cases) against a cost of 0.19 %. Against the coin's upward drift (-0.41 % in the short direction) the total move is -0.28 %, so no change of holding, sizing or threshold can make this signal pay.
- F5: The give-back appears only when the coin is not already far above its 30-day level.
- F6: The effect lives in falling-market years: +1.52 % unusual fall in 2018 (t 3.83, 712 cases) and +0.89 % in 2022 (t 3.02, 711 cases), against -0.82 % in 2020 (t -2.38, 720 cases) and -0.43 % in 2021.
