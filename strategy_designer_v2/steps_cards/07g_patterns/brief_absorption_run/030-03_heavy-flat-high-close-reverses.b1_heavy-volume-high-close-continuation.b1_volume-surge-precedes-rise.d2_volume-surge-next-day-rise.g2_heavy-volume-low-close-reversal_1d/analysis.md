---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6156 USD
---
## Findings
- **F1:** The tested link is concentrated in its extreme corner. Days with volume over 2.5 times the prior 20-day mean that closed in the bottom fifth of their range were followed by a next-day excess return of +3.19 % (t 4.14, 102 cases), and those with volume 1.5–2.5 times by +1.05 % (t 3.41, 310 cases). Every other volume-by-close cell sits between −0.55 % and +0.42 %, with |t| below 1.6. With volume over 2 and close location above 0.8, all six coins are positive (+1.25 % to +3.37 %) and seven of eight years are positive.
- **F2:** On the tested product of close location and volume ratio, the top quintile's excess return over the next two days, on a non-overlapping 2-day grid, is +0.92 % (t 4.29, 1445 cases). The other four quintiles are all negative (−0.13 % to −0.35 %). On the 3-day grid the top quintile gives only +0.58 % (t 1.88), so the move is mostly over within two days.
- **F3:** On down days, the wider the range against the prior 20-day mean range, the higher the next-day excess return (slope t 6.06, 7144 down days). Up days show no such rise: the widest-range quintile gives −0.27 %, t −1.65.
- **F4:** In the widest-range quintile of down days, the next-day excess return is positive in all six coins (+0.54 % to +1.22 %, t 1.43 to 3.78) and in all eight years (+0.17 % to +1.70 %). Within that quintile, heavy-volume days give +1.16 % (t 5.41, 864 cases) and normal-volume days +0.35 % (t 1.61).
- **F5:** Measured in units of the coin's prior 20-day volatility, falls of 1 to 1.5 are followed by +0.62 % (t 3.52, 861 cases) and falls of 2 to 3 by +0.61 % (t 2.34). Small rises of 0 to 1 are followed by about −0.2 % (t −2.3 to −2.5).
- **F6:** In a joint regression of the next-day excess return, close location × volume ratio keeps t 6.30 and the size of the fall in volatility units keeps t 2.50. The range ratio is negative (t −2.87) when up and down days are pooled.
- **F7:** Among days falling more than 1.5 volatility units, heavy-volume days that closed in the bottom 30 % of their range gave +1.60 % next day (t 4.70, 331 cases). The other three groups were within ±0.7 % (|t| ≤ 1.34).
- **F8:** The book's daily returns track the coins closely (correlation 0.77, slope 0.39). Positions average 0.42 and are above 0.01 on 88 % of bars. The middle forecast quintile still holds 0.25 while its next-day excess return is −0.14 %, so ordinary days are held at a cost.
- **F9:** The next-day excess return after the Friday bar is +0.30 % (t 3.76, 2479 cases), positive in all six coins. It is negative in 2018, 2022 and 2023, and among seven weekdays it does not stand out enough to count.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal.g1_wide-range-down-day-rebound` (from F3, F4, F6): On a day that falls, the wider that day's high-low range is against the coin's average range over the prior 20 days, the more the coin rises over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal.g2_absorption-rebound-over-two-days` (from F1, F2, F8): On a day of heavy volume against the coin's prior 20-day average, the lower the close sits within the day's high-low range and the heavier the volume, the more the coin rises over the next two days.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal.g3_volatility-scaled-capitulation-rebound` (from F5, F6, F7): The larger a coin's one-day fall against its own 20-day volatility, and the lower that day's close sits within its range on heavy volume against its prior 20-day average, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
