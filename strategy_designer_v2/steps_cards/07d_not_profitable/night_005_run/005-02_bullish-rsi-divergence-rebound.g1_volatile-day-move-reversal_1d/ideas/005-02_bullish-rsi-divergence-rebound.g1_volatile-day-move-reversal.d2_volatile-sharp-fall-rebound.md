---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high, a large one-day fall is followed by a rebound over the next 3 days. The larger the fall relative to the coin's usual daily move, the larger the rebound.
Consequence: Buying a volatile coin after a sharp down day captures a graded rebound without the losses of shorting its rallies.
Why:
- F4: The fade is graded in both directions. Excess 3-bar return runs from +0.0144 (t 1.98, n 124) after the largest vol-scaled falls (mean z −2.17) to −0.0134 (t −2.62, n 124) after the largest rises (mean z +2.41). The slope on up days has t −3.40 (n 404), and on down days t −1.29 (n 340).
- F5: Longs taken after a down day earned on bars in both trends: +0.00276 per bar (t 2.07, n 634) when the 20-day return was negative and +0.00185 (t 1.50, n 481) when it was positive. The book's weakness is on the short side, not the long side.
- F6: The book trails holding because it stays out or short through the coins' rises. Flat days missed a mean coin return of +0.00219 (n 2086) and short days earned only +0.00005. The book's market-rise gain is about zero (−0.00003 BTC, −0.00001 ETH) against coin means of 0.00118 and 0.00137. Fees take 0.00031 of the 0.00069 mean gain per bar, and the three smallest forecast quintiles earn less than their fees.
