---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the more often that level turned the price down and the farther the close sits above it, the larger the rise.
Consequence: A trader should size a break by how often the level held and how clearly it was cleared, not by the run before it, and give barely-cleared, rarely-tested levels little or nothing.
Why:
- F1: The book fails on its falls, not on its gain. Its deepest fall is 33.6 % against a yearly return of 24.9 %, a Calmar of 0.741 against the 0.75 required, while its Sharpe is 1.02 and it beats holding by 0.44. That fall runs 623 days across w1 to w6, and the next falls are 27.7 % (w12 to w15) and 22.8 % (w16 to w17).
- F5: Weak breaks carry no rise, and the strength of the break grades the rise. Trades in the lowest fifth of the break reading (touch count × margin, mean 0.45) returned −0.5 % per trade; the top fifth (mean 11.6) returned +7.4 %, and the middle fifths +0.6 % to +2.4 %. Leaving out weak-break days together with falling-month days takes the deepest fall to 20.7 % and the Calmar to 1.20; this is also in-sample.
- F6: The 10-day run before the break grades the 5-day rise only weakly. By fifth of the 10-day return, the 5-day return runs −0.1 %, 2.0 %, 0.5 %, 1.2 %, 1.6 %. Measured against the coin's 20-day volatility, the 10-day run gives no ordered pattern in return per trade (1.7 %, 4.1 %, 0.0 %, 6.3 %, 3.0 %).
- F8: The idea is large enough to pay its costs. Per case, the unusual move of +0.43 % over 5 days is 1.9 times the 0.22 % round trip, and the total move of +1.17 % is 5.2 times it. The book's shortfall is in when it is long, not in the size of the move it bets on.
