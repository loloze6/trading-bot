---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose daily volatility over the past 20 days is high, a down day is followed by a rise over the next 1 day, and that rise grows more than in proportion to the fall measured in the coin's 20-day daily standard deviations, so shallow falls are followed by almost no rise. The rise is largest when the fall extends the coin's decline over the prior 4 days, and it grows with the depth of that 4-day decline.
Consequence: Put the long only behind deep falls that cap a multi-day slide in a volatile market, and leave shallow single-day dips alone, where the fees outweigh the rebound.
Why:
- F1: Almost all of the book's edge sits in its deepest-fall bars. In the top forecast quintile (forecast 14.5–20, allocation 0.91) each active bar gains 0.0090, with next-day return 0.0120 and t 5.30. The middle three quintiles gain only 0.0005–0.0020 per bar.
- F2: Fees eat most of the shallow-fall positions. The lowest forecast quintile pays a fee of 0.00008 per bar against a gain of 0.00008. The second and third quintiles pay 0.00021 and 0.00030 against gains of 0.00050 and 0.00063. The 3366 trades average −0.11% before fees and −0.21% after. The book's mean daily return is 0.00045, against 0.00118 for holding the coins.
- F3: The reversal grows much faster than the fall's size. In the high-volatility regime, falls beyond 2 standard deviations are followed by 0.0201 next day (n 124), falls of 1–1.5 by 0.0106 (n 416), and falls of 0–1 by only 0.0034–0.0038.
- F4: The high-volatility regime is what makes falls reverse. The same falls beyond 2 standard deviations in the calm regime are followed by only 0.0013 (n 287), and falls of 1.5–2 by 0.0009 (n 278).
- F5: Among falls beyond 1 standard deviation, the reversal depends on the four days before the fall. After the steepest prior 4-day declines the next day returns 0.0168 (t 5.06, n 459). After a flat prior 4 days it returns −0.0038 (t −1.78, n 458).
- F7: The book's losses come from big positions on mid-sized falls that keep going. The worst 5% of active bars carry allocation 0.78 against 0.39 overall, and a day's fall of −1.30 standard deviations against −0.55. All of them sit in the high-volatility regime, and the book's deepest fall is −22.6% (Calmar 0.70).
