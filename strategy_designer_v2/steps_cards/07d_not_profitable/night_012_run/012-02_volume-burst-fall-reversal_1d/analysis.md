---
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
idea tested: 012-02_volume-burst-fall-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3735 USD
---
## Findings
- **F1:** The book fails on size, not on direction: its mean daily return is 0.000379 (the rule needs 0.0005) against 0.00118 for holding the coins, because it holds a position on only 20.7 % of bars, at a mean allocation of 0.48; the part of its gain that comes from the market's own rise is only 0.000118 per bar.
- **F2:** Nearly all of the book's gain comes on the first day after a signal. On those 3040 bars the mean gain is 0.00325 and the coin's next-day return is 0.0057. On days 1 to 3 after the signal the coin's next-day return is negative (−0.0021, −0.0034, −0.0083; 325, 154 and 66 bars).
- **F3:** Trade length points the same way. Trades of up to 1.5 days net +1.48 % (1859 trades), while trades of 1.5–3.5 days net −4.83 % (433) and trades of 3.5–7.5 days net −6.99 % (196); overall the 2812 trades net −0.17 % on average.
- **F4:** The rebound sits almost wholly in the strongest forecasts. Signal bars in the top forecast quintile (mean volume ratio 1.89) are followed by a 3-day return of 0.0127. The four lower quintiles give −0.0008 to 0.0042, which is no larger than the coin's own mean.
- **F5:** The losses depend on the 30-day trend. Signal bars in the second-lowest 30-day-return quintile (mean −0.128) are followed by a 3-day return of −0.0036, and held bars there lose −0.00065 a bar. The top quintile (30-day return +0.44) gives a 3-day return of +0.0105 and held bars there gain +0.0039; the deepest-fall quintile (−0.32) also rebounds, at +0.0067.
- **F6:** The deepest falls (largest drawdown −0.238 in w9, Calmar 0.516) gather in falling markets. The worst 5 % of position bars (182, mean −8.1 %) come almost all on the signal day itself. They have a mean 10-day return of −0.068, and 54 % of them have a negative 30-day return, against 43 % of all held bars.
- **F7:** A deeper lower wick does not add to the rebound. Signal bars in the deepest-wick quintile (wick 0.63 of the range) are followed by 0.0027 over 3 days, against 0.0078 in the shallowest quintile.

## Ideas
- `012-02_volume-burst-fall-reversal.d1_one-day-volume-flush-rebound` (from F2, F3, F4): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, with the rebound spent by the second day.
- `012-02_volume-burst-fall-reversal.d2_volume-flush-in-uptrend` (from F5, F6, F4): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 3 days, and the higher the coin's 30-day return before the fall, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
