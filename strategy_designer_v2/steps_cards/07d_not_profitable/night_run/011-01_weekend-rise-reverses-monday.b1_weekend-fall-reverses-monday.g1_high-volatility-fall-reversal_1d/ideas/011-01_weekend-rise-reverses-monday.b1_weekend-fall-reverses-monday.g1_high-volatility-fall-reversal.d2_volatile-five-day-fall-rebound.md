---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose daily volatility over the past 20 days is high, the coin rises over the next 1 day, and the rise is larger the deeper the coin's 5-day fall.
Consequence: After a sharp multi-day sell-off in a volatile market, lean long for the next day, harder the deeper the 5-day fall.
Why:
- F4: The high-volatility regime is what makes falls reverse. The same falls beyond 2 standard deviations in the calm regime are followed by only 0.0013 (n 287), and falls of 1.5–2 by 0.0009 (n 278).
- F5: Among falls beyond 1 standard deviation, the reversal depends on the four days before the fall. After the steepest prior 4-day declines the next day returns 0.0168 (t 5.06, n 459). After a flat prior 4 days it returns −0.0038 (t −1.78, n 458).
- F6: The coin's 5-day return grades the next day across all active bars. The bottom 5-day-return quintile (−56% to −10%) gives a next-day return of 0.0110 (t 4.00). The flat quintile (−4% to 0%) gives −0.0005 (t −0.36), even though allocation there is a similar 0.39.
