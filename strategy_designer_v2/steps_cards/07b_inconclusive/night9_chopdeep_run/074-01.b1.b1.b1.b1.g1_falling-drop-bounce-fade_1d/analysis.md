---
line: 7.b inconclusive
backtest: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2615 USD
---
## Findings
- **F1:** The supporting check failed because the forecast hit its cap, not because the effect is ungraded: 69 % of the 160 cases in folds B and C (median forecast -20, mean -18.8) sit at the -20 cap, so no cases are above the median size and step 5's check returned None. Meanwhile the main measure is on the predicted side: an unusual short move of +2.26 % per case, t 2.47, on 79 days, strength 0.40.
- **F2:** Inside the tested situation, which already requires a fall of at least one usual 5-day move, the next-day fall does not grow with depth. By prior 5-day fall tercile it is +3.25 % (shallow, t 2.80), +0.80 % (mid, t 0.62) and +2.66 % (deep, t 1.65). By forecast tercile it is +2.84 %, +1.80 % and +2.15 %. The threshold has removed the gradient the idea claims.
- **F3:** Across all wide up days in a falling market, whatever the prior week (390 cases, 160 days, +1.01 %, t 2.24), the next-day fall grows with the depth of the previous 5-day move, measured in usual 5-day moves:
- **F4:** On the same 390 wide up days in falling markets, the next-day fall also grows with the day's width against its 20-day mean range: +0.41 % (t 0.63), +0.88 % (t 1.39) and +1.75 % (t 2.45, strength 0.31) from the least wide to the widest tercile.
- **F5:** The fade is broad, not carried by one coin or one period. It is positive on 10 of 12 coins, with ETH at +3.21 % (t 3.99), BTC +2.79 % (t 2.46), LTC +2.36 % (t 2.52) and ZEC +2.12 % (t 2.33). It is also positive in 8 of 10 windows. The test already used every coin and fold available, so there is no more data to add.

## Ideas
- `074-01.b1.b1.b1.b1.g1.b1_falling-wide-bounce-depth-graded` (from F1, F2, F3, F5): In a falling market, a wide up day is followed by a fall over the next day, and the deeper the coin's fall over its previous 5 days, the larger the next day's fall.
- `074-01.b1.b1.b1.b1.g1.b2_falling-wide-up-day-width-fade` (from F3, F4, F5): In a falling market, an up day whose high-low range is wide against the coin's mean daily range of the last 20 days is followed by a fall over the next day, and the wider the day, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
