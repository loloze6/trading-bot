---
line: 7.g patterns
backtest: 032-02_volatile-decline-low-rebound_1d
idea tested: 032-02_volatile-decline-low-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3761 USD
---
## Findings
- **F1:** Over 5 days, a coin whose close sits closest to its prior 30-day high goes on to rise more than its normal drift: in the top quintile of the close-to-prior-30-day-high distance (mean −2.3 %), the unusual 5-day move is +3.60 % (t 3.09 with cases of one day taken together, 247 cases on 91 days). The other quintiles run from −2.72 % to −0.11 %, and the second-lowest is the weakest at −2.72 % (t −2.53).
- **F2:** The effect is graded but not cleanly monotonic. The slope of the unusual 5-day move on each coin's rank of that distance is +0.053 per unit rank (t 2.20, 230 days), even though the second-lowest quintile is weaker than the lowest.
- **F3:** The same pattern appears for other lookbacks. On the 10-day high, the top quintile is +3.14 % (t 3.08, 111 days) with slope t 2.39. On the 60-day high, the top quintile is +3.19 % (t 2.47, 57 days). The position within the 30-day high-low range gives +2.50 % (t 1.92).
- **F4:** The top-20 % vs rest gap in the unusual 5-day move is positive in all 6 coins and in 10 of 12 windows. By coin it runs from +2.26 % (LTC) to +11.60 % (XRP); w7 (−1.47 %) and w9 (−1.10 %) are the two exceptions.
- **F5:** The near-high rise is strongest when the coin's 20-day volatility is in its lower half: +3.85 % (t 3.19, 66 days), against +3.02 % (t 1.35, 52 days) in the upper half.
- **F6:** The tested rebound does not show in falling, volatile markets. Among bars with a negative 30-day return and 20-day volatility above the coin's median, every quartile of distance above the prior 30-day low has a negative unusual 5-day move (−2.46 % to −0.46 %; the strongest t is −2.45). That whole regime averages −1.18 % (t −1.76, 325 cases).
- **F7:** The size of the effect is large against costs. The +3.60 % per case in F1 is about 19 times the 0.19 % cost of a trade (buy plus sell). Weekday effects (Monday +1.58 %, t 2.20; Thursday −1.61 %, t −2.13) do not stand out given the more than 15 cuts examined, and are not counted.

## Ideas
- `032-02.g1_near-monthly-high-continuation` (from F1, F2, F3, F4, F7): In a coin, the closer its daily close sits to (or above) the highest high of its prior 30 days, the larger its rise over the next 5 days.
- `032-02.g2_calm-breakout-continuation` (from F1, F5): When a coin's daily returns over the past 20 days have been calm compared with its own past year, the closer its close sits to the highest high of its prior 30 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
