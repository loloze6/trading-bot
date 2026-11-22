---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves, and the wider that 30-day high-low range is against its close, the larger that fall.
Consequence: A moderate slide in a flat coin is a short worth more the wider the coin's monthly range, and almost nothing in a tight range.
Why:
- F1: Each case's move does not pay for a trade. Over 5 days the unusual move is +0.55 % per case, but the coin's normal drift against the short is -0.79 %, so the total move is -0.24 % against a cost of 0.22 %. On the 928 grid cases the short's total move is +0.21 % (t 0.62), and the book's mean daily return is -0.0078 %, of which the market's own rise accounts for -0.0146 % a day.
- F3: The effect is absent where the book is largest. In the narrowest quarter of 30-day range width (high-low over close), the unusual move is -0.47 % (strength -0.05) with a total move of -1.23 % (t -2.58, 167 cases), and the short there averages an allocation of -0.43. In the three wider quarters the unusual move is +1.8 % to +2.1 % (strength 0.13 to 0.18) with a total move of +1.1 % to +1.3 %.
- F4: Volatility grades the move the same way. In the calmest quarter of 20-day volatility the unusual move is +0.01 % (total -0.73 %, t -1.55, 192 cases). In the third quarter it is +3.0 % (total +2.2 %, t 2.97, 191 cases).
