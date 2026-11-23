---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3788 USD
---
## Findings
- **F1:** On days that close in the lowest quarter of their range, the next-day excess return grows steadily with the day's volume against its prior 20-day mean: about zero below 1.5 times the mean (-0.09 %, +0.13 %, +0.23 %; n 1127, 692, 668). It is +0.94 % from 1.5 to 2 times (t 2.86, n 291), +1.32 % from 2 to 3 times (t 4.11, n 175) and +3.74 % above 3 times (t 3.69, n 83).
- **F2:** The slope of the next-day excess return on the close's location (1 at the low) rises with the volume ratio: 0.0004 below 0.7 times (t 0.20, n 5644), 0.0097 at 1.5-2 times (t 1.82), 0.0174 at 2-3 times (t 2.78, n 846) and 0.0438 above 3 times (t 3.18, n 446). The book's cut at twice the mean drops part of a graded effect.
- **F3:** On heavy days (at least 2 times volume) closing in the lowest quarter, the next-day excess return grows with the day's range against its prior 20-day mean range: +0.98 % (t 2.20), +2.17 % (t 3.48) and +3.15 % (t 3.49) across the range-ratio terciles, about 86 cases each.
- **F4:** On days of any volume closing in the lowest quarter, a fall of 1 to 2 of the coin's 20-day daily standard deviations is followed by +0.61 % next-day excess (t 3.64, n 933). A fall of more than 2 is followed by +1.21 % (t 3.35, n 284). A fall of less than 1 is followed by +0.03 % (t 0.32, n 1689).
- **F5:** The heavy-volume low-close rebound holds across every coin, at +1.26 % to +3.27 % next-day excess (t 1.50 to 3.15, 35-55 cases each), and is positive in every year 2018-2025 (+0.29 % to +6.27 %). The book's 783 cases make a total move of +0.82 %, 4.3 times the 0.19 % cost of a trade.
- **F6:** The rebound is mostly over within a few days. Heavy low-close days show +2.44 % excess over 3 days (t 2.76, 72 cases), but only +0.61 % over 5 days (t 0.62, 56 cases).
- **F7:** The book's gain rests on its tails. Over 4191 active coin-days, summing to +3.81, the best 5 % of days sum to +7.96 and the worst 5 % to -5.12.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound.g1_volume-graded-low-close-rebound` (from F1, F2, F5): The further a day's volume sits above its 20-day average, the more the coin rises over the next 1 day after a close near the day's low. The effect grows continuously through moderately heavy days to the heaviest ones.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound.g2_wide-range-low-close-rebound` (from F3, F5): On a heavy-volume day that closes near its low, the wider the day's high-low range against its 20-day average range, the more the coin rises over the next 1 day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound.g3_volatility-scaled-down-close-rebound` (from F4, F6): The larger a day's fall, measured in the coin's 20-day daily volatility, on a day that closes near its low, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
