---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the last 1 day, the higher its return over the next 1 day, only while the coin's realised volatility over the last 20 days is high against its last 60 days, the rebound growing with that ratio.
Consequence: A trader would buy one-day drops in proportion to the drop and to how expanded recent volatility is, and would refuse to buy drops that come out of a quiet, compressed market.
Why:
- F1: The book fails only on Calmar: 0.698 against the 0.75 bar. Its daily chain returns 18.5 % a year with a deepest fall of -26.6 % (w8 into w9, 119 days to the trough). The other deep falls are mostly in falling markets: in w16 the book lost a summed -0.26 while the coins summed -0.82, and from w12 to w14 it lost -0.21 while the coins summed -0.78.
- F2: The rebound after a one-day drop is absent when recent volatility is compressed. In the lowest quintile of 20-day over 60-day realised volatility, active bars have a next-day excess return of -0.0033 (t -2.60, n 1431), a mean position gain of -0.0010 and a slope on the forecast of -0.00016 (t -0.68). In the highest quintile the excess return is +0.0063 (t 4.61) and the slope is +0.00059 (t 2.96). The gain rises steadily across the quintiles (-0.0010, 0.0012, 0.0021, 0.0024, 0.0046).
- F3: The interaction regression of next-day excess return on forecast, volatility ratio and their product gives the product a t of 3.45. The forecast alone gets a t of -2.37. So the drop's size predicts a rebound only in proportion to how expanded recent volatility is.
- F5: Scaling each position by the volatility ratio (clipped 0 to 2) lifts the pre-fee book from a mean of 0.00092 to 0.00112 and a yearly return from 34.4 % to 44.0 %. Calmar rises from 1.45 to 1.90, but the deepest fall barely moves (-23.8 % to -23.2 %). The Calmar gain comes through the yearly return, not through shallower falls.
- F6: The book's worst 5 % of days lose about evenly across the volatility-ratio quintiles (summed losses of -4.5, -4.0, -5.5, -5.4 and -6.0). The deep falls are therefore not confined to compressed markets.
