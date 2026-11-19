---
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2672 USD
---
## Findings
- **F1:** The main measure is on the predicted side but too noisy for 195 cases: the mean signed 72-hour excess return is 0.0075 with t 1.35, a standard deviation of 0.077, a positive share of only 52.8 % and a median of 0.0046, so at this mean and spread about 426 independent cases would be needed to reach t = 2.
- **F2:** The give-back shows more clearly over shorter horizons than the plan's 3 days: over 24 hours it is 0.0058 with t 2.79 on 628 cases (BTC 0.0048 with t 2.04 on 313, ETH 0.0069 with t 1.98 on 315), over 48 hours 0.0067 with t 1.90 on 321, and over 72 hours 0.0075 with t 1.35 on 195.
- **F3:** At 72 hours both coins point the same way but neither is clear on its own: BTC 0.0050 with t 0.95 on 96 cases and ETH 0.0098 with t 1.02 on 99.
- **F4:** One year pulls the 72-hour result down: 2018 gives −0.0387 with t −1.93 on 23 cases, 6 of the 8 years are positive, and without 2018 the mean is 0.0136 with t 2.48 on 172 cases.
- **F5:** The long side carries most of the 72-hour effect: going long after a fall gives 0.0131 with t 1.72 on 99 cases, against 0.0016 with t 0.21 on 96 cases for going short after a rise.
- **F6:** The grading is only partly there at 72 hours. The mean signed excess return rises from 0.0003 (t 0.09, 479 cases) for |forecast| up to 2.5, to 0.0088 for 5 to 10, and to 0.0133 for 10 to just under 20. It then falls back to 0.0050 (t 0.73, 138 cases) for the capped forecast of 20.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.b1_volatile-reversal-more-coins` (from F1, F3, F4): In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next 3 days. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over those 3 days.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.b2_volatile-day-move-one-day-reversal` (from F2, F1): In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next day. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over that next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
