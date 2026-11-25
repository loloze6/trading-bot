---
line: 7.g patterns
backtest: 042-01_low-close-next-day-rebound_1d
idea tested: 042-01_low-close-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4523 USD
---
## Findings
- **F1:** In folds B and C the close's place in the range works only on wide days. Split by the day's range against its own 20-day mean, the slope of the next-day drift-removed z on close location (1 at the low) is 0.008 (t 0.13) in the narrowest tercile, 0.17 (t 2.49) in the middle one and 0.44 (t 6.01) in the widest, 2656 bars each. Clustered by day, the close-location × log relative-range interaction is +0.44 (t 2.79, 1328 days).
- **F2:** On the widest-range quintile the move is many times the 0.19 % cost of a trade. The next day, drift removed, is +1.22 % when the close sits in the lowest third of the range (684 cases) and −0.96 % when it sits in the highest third (524 cases). Across all days the move is +0.22 % per case.
- **F3:** Close location adds nothing beyond the day's own return.
- **F4:** The effect lives in markets that are not rising, using the 60-day trend.
- **F5:** The effect is one day long and fades after that. The non-overlapping close-location slope is −0.04 (t −0.62, 2862 cases) at 3 days and −0.17 (t −1.87, 1710 cases) at 5 days. The wide-day weighted version still holds over 2 days, at 0.17 (t 2.40, 714 days).
- **F6:** The wide-day weighted version points the same way on every coin, with day-clustered t of 2.43 (BTC), 2.71 (ETH), 2.80 (LTC), 4.23 (XMR), 1.37 (XRP) and 3.48 (ZEC).
- **F7:** The weekday split is a single striking but isolated reading among many angles, and it is unclustered. The close-location slope is −0.31 (t −3.17) on Monday bars and −0.00 on Tuesday bars, against 0.32 to 0.42 (t 2.8 to 4.4) on the other five days.

## Ideas
- `042-01.g1_wide-day-low-close-rebound` (from F1, F2, F5, F6): A coin rises over the next day, more so the nearer that day's close sits to its low and the wider that day's high-low range is against its range over the past 20 days.
- `042-01.g2_falling-market-low-close-rebound` (from F4, F1, F2): In a falling market, a coin rises over the next day, more so the nearer that day's close sits to its low, and more so the wider that day's high-low range is against its past 20 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `042-01.g3_one-day-fall-next-day-rebound` (from F3): A coin rises over the next day, more so the larger that day's fall is against the coin's usual one-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
