---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3225 USD
---
## Findings
- **F1:** The gain sits only in the largest scaled moves: among active bars, the top quintile of |day's return / 20-day volatility| (mean |z| 1.87) earns 0.00477 a bar before fees (t 2.77, n 574) and 0.00406 after fees. The four lower quintiles earn 0.00009 to 0.00103 before fees against fees of 0.00031 to 0.00053, so three of the four lose net (-0.00022, -0.00010, -0.00040).
- **F2:** Fees eat 42% of the gain: across all bars they cost 0.000279 a bar against a gross gain of 0.000669. Trades come at 0.40 per bar, and in ETH's deepest fall the fees summed to 0.23 against a gain sum of -0.12.
- **F3:** Among high-volatility bars in the top two |z| quintiles, the move back holds only when the day ran against the coin's 20-day return.
- **F4:** The book carries almost no gain from the market's own rise (drift part -0.000017 a bar), so it trails holding in rising years: in 2020 the book earned 0.00024 a day against the coin's 0.00524, and in 2021 0.00045 against 0.00382. This is why its Sharpe is 0.15 below holding's.
- **F5:** The deepest falls are long and slow rather than single shocks.
- **F6:** The gain rises with the volatility ratio: in the top quartile of 20-day volatility over its 60-day mean, active bars earn 0.0060 long and 0.0024 short. The lower quartiles earn between -0.0012 and +0.0017.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.d1_counter-trend-volatile-day-reversal` (from F3, F1, F5): On a coin's high-volatility days, measured by its 20-day volatility, the next day's return runs against the day just closed, only while that day's move runs against the coin's 20-day return. The larger that day's return relative to its 20-day volatility, the larger the move back over the next 1 day.
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.d2_volatility-expansion-graded-one-day-reversal` (from F6, F1, F2): On a coin's high-volatility days, measured by its 20-day volatility, the next day's return runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the higher the 20-day volatility stands above its 60-day average, the larger the move back over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
