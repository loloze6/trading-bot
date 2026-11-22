---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves, and the more negative its 60-day return, the larger that fall.
Consequence: A flat coin's moderate slide is a short to take when the coin has been losing over the past two months, where its fall beats both the coin's usual rise and the trade's cost.
Why:
- F1: Each case's move does not pay for a trade. Over 5 days the unusual move is +0.55 % per case, but the coin's normal drift against the short is -0.79 %, so the total move is -0.24 % against a cost of 0.22 %. On the 928 grid cases the short's total move is +0.21 % (t 0.62), and the book's mean daily return is -0.0078 %, of which the market's own rise accounts for -0.0146 % a day.
- F5: The total move turns positive when the coin's 60-day return is weakest. In the lowest quarter of 60-day return the unusual move is +2.9 % and the total move +2.0 % (t 2.29, 107 cases).
