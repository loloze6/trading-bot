---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3401 USD
---
## Findings
- **F1:** The deepest falls come from shorting rising coins. In BTC's worst fall (−68%, 1171 days) and ETH's (−54%, 498 days), the coins rose 151% and 171%, and the short side lost 0.93 and 0.75 while the long side gained 0.33 and 0.25. The short side alone has a Sharpe of −0.04 and a deepest fall of −70% in BTC, against 0.90 and −33% for the long side.
- **F2:** Shorts held while the coin's 20-day return was positive lost on average (book −0.00168 per day, t −2.25, n 863). Shorts held while it was negative earned (+0.00228, t 3.52, n 780). Longs in a rising coin earned +0.00329 (t 4.10, n 697).
- **F3:** On the non-overlapping 3-bar grid in the active regime, the give-back after an up day is concentrated where the 20-day return is negative: excess 3-bar return −0.0117 (t −2.41, n 188). Where the 20-day return is positive it is −0.0010 (t −0.27, n 216).
- **F4:** The fade is graded in both directions. Excess 3-bar return runs from +0.0144 (t 1.98, n 124) after the largest vol-scaled falls (mean z −2.17) to −0.0134 (t −2.62, n 124) after the largest rises (mean z +2.41). The slope on up days has t −3.40 (n 404), and on down days t −1.29 (n 340).
- **F5:** Longs taken after a down day earned on bars in both trends: +0.00276 per bar (t 2.07, n 634) when the 20-day return was negative and +0.00185 (t 1.50, n 481) when it was positive. The book's weakness is on the short side, not the long side.
- **F6:** The book trails holding because it stays out or short through the coins' rises. Flat days missed a mean coin return of +0.00219 (n 2086) and short days earned only +0.00005. The book's market-rise gain is about zero (−0.00003 BTC, −0.00001 ETH) against coin means of 0.00118 and 0.00137. Fees take 0.00031 of the 0.00069 mean gain per bar, and the three smallest forecast quintiles earn less than their fees.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d1_fade-rises-only-in-downtrends` (from F1, F2, F3, F5): In a coin whose 20-day volatility is high, a large one-day move is partly given back over the next 1 to 3 days, only when the move runs against the coin's 20-day return. A rise is given back while the coin's 20-day return is negative, and a fall is given back in any trend. The larger the day's move and the higher the coin's 20-day volatility relative to its usual level, the larger the opposite move that follows.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d2_volatile-sharp-fall-rebound` (from F4, F5, F6): In a coin whose 20-day volatility is high, a large one-day fall is followed by a rebound over the next 3 days. The larger the fall relative to the coin's usual daily move, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
