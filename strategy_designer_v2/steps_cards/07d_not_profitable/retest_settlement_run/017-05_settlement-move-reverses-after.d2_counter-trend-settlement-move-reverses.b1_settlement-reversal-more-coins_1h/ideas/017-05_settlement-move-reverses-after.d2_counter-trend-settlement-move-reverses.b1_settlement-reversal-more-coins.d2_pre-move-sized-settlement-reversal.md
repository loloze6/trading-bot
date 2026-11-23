---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 2 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend. The larger the 2-hour pre-move relative to the coin's usual hourly move, the larger the move back.
Consequence: A trader sizes the settlement reversal by the size of the move into settlement, not by the trend, and exits within 2 hours, before the move back fades.
Why:
- F1: The move back after settlement is short-lived, and the 8-hour hold throws it away. On settlement bars where the 2-hour move runs against the 24-hour trend, the drift-adjusted return in the trend's direction is +0.033 % after 1 h (t 6.2), +0.062 % after 2 h (t 8.5) and +0.041 % after 4 h (t 4.2). By 8 h it falls to +0.009 % (t 0.68), and by 16 h it is −0.084 % (t −4.1); there are 44,575 cases.
- F3: The settlement clock carries the effect, and it scales with the size of the pre-move. At 2 h, counter-trend cases at settlement earn +0.062 % against +0.015 % at non-settlement 4-hourly bars (47,404 cases).
- F5: With an 8-hour hold, the trend's strength alone does not grade the move. Across trend-strength quintiles the 8-hour returns are +0.039, −0.004, −0.023, −0.061 and +0.082 %, which is not monotonic. Pre-move-size quintiles at 8 h rise only at the top (+0.099 %, t 2.6).
