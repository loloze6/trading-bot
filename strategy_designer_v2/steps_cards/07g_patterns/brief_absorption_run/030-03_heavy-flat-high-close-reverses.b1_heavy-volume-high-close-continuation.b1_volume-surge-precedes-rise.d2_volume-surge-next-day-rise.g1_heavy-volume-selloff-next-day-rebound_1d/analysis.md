---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3998 USD
---
## Findings
- **F1:** Among down days on volume at or above the prior 20-day mean, where the close sat in the day's range sorts the next day sharply. Closes in the lowest third of the range were followed by +0.64 % excess (t 4.81, n 1553). Middle-third closes gave +0.23 % (t 1.21, n 955) and top-third closes gave −0.26 % (t −0.84, n 210). Light-volume down days closing low gave −0.02 % (t −0.19, n 2388). The tested idea's rebound is therefore carried by heavy down days that close near their low, which the idea does not name.
- **F2:** The same pattern shows in the lower wick. Heavy down days in the smallest lower-wick tercile (close near the low, no buying-back intraday) gave +0.90 % next-day excess (t 5.19, n 950). The middle and largest wick terciles gave only +0.17 % (t 1.01) and +0.17 % (t 0.87).
- **F3:** Among the bottom fifth of daily returns, the next-day excess grows with the volume ratio: +0.02 % (t 0.09), +0.42 % (t 2.17), +0.32 % (t 1.66) and +1.14 % (t 4.66) from the lowest to the highest quartile, about 725 cases each. It also grows with 20-day volatility on heavy days: −0.08 % (t −0.37), +0.35 % (t 1.72) and +1.54 % (t 5.25) from the low to the high tercile. This repeats the tested idea's grading.
- **F4:** The rebound is a one-day move. On active bars the excess from day 1 to day 2 is +0.07 % (t 0.66, n 2694), against +0.42 % on day 1.
- **F5:** Active bars on a Saturday were followed by +1.55 % next-day excess (t 4.70, n 170), and on a Sunday by +1.22 % (t 2.17, n 175). Weekday active bars ranged from −0.03 % to +0.79 %, about 440 to 490 each. All bars by weekday show nothing of this size on Saturday: +0.04 % (t 0.42).
- **F6:** On the book's worst 5 % of days (book −6.0 %, coin −8.8 %, n 287), the coin rose +1.80 % and the book +1.15 % the next day. On its best 5 % (coin +9.9 %), the coin fell −0.47 % the next day. Large coin falls are followed by part-reversal; large rises are not followed by a comparable fall.
- **F7:** The rebound after heavy falls holds in every year, from +0.05 % (2022, t 0.17) to +1.21 % (2021, t 3.17). It also holds in every coin, from +0.22 % (BTC, t 1.30) to +0.61 % (XMR, t 2.59).
- **F8:** The mirror on up days is weaker than the rebound and does not stand out across this many angles. Top-fifth up days in the high-volatility tercile gave −0.56 % on heavy volume (t −2.21, n 644) and −0.36 % on light volume (t −1.85). Heavy up days closing in the top third gave −0.01 % (t −0.11).

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low` (from F1, F2, F3, F4): The nearer a coin closes to its day's low on a down day whose volume is heavy against its prior 20-day average, the more it rises over the next day. The heavier the volume, the larger that rise.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound` (from F5, F3, F4): The more a coin falls on a Saturday or Sunday whose volume is heavy against its prior 20-day average, the more it rises over the next day. That rise is larger than after the same fall on a weekday.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound` (from F2, F1, F3): The larger the share of a day's fall that remains at the close, measured as how small the lower wick is against the day's range, the more the coin rises over the next day. This holds on down days whose volume is heavy against the prior 20-day average, and more so when 20-day volatility is high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
