---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls, and that fall shows within the next 5 days and is gone after them.
Consequence: A short taken on a flat coin's slide earns its move within five days, so a trader who is still short after that is paying for the coin's usual rise.
Why:
- F2: The book holds the short long after the signal has gone. 65 % of short bars have a forecast of 0, and they lose -0.036 % per bar, while short bars with a negative forecast gain +0.011 %. Trades last 8.2 days on average, and the 249 trades held over 20 days lose -25.1 % gross on average (median +3.8 %).
- F1: Each case's move does not pay for a trade. Over 5 days the unusual move is +0.55 % per case, but the coin's normal drift against the short is -0.79 %, so the total move is -0.24 % against a cost of 0.22 %. On the 928 grid cases the short's total move is +0.21 % (t 0.62), and the book's mean daily return is -0.0078 %, of which the market's own rise accounts for -0.0146 % a day.
