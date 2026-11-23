---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a down day relative to its own prior 20-day average, and the larger that day's fall, the more the coin rises over the next day, whether or not it had already fallen over the previous 20 days.
Consequence: A trader buys a heavy-volume fall for one day in any trend, weighting by the volume multiple rather than by the prior 20-day decline, which avoids buying quiet dips inside strong rallies.
Why:
- F1: The book's gain comes from the heavy-volume part of the signal; on low-volume falls the edge is smaller than one trade's cost. Held bars after a volume ratio of 1.5–2.5 earned +0.64 % per bar (466 bars), and after a ratio above 2.5 they earned +0.94 % (194 bars). After a ratio of 1 or less they earned only +0.11 % (2210 bars, more than half of all held bars), and from 1 to 1.5 they earned +0.06 % (700 bars). One trade costs 0.19 %.
- F3: The prior 20-day decline adds little to the rebound, so it does not grade the effect; volume does. On down days with volume above 3 times the 20-day average, the next-day excess return is +1.75 % without the signal (83 cases) and +1.45 % with it (125 cases). For ratios 2–3 it is +0.39 % without against +0.79 % with. On down days in a 20-day decline with volume above 1.5 times average, the excess is +0.98 % with or without the signal (110 / 622 cases). On ratios of 1 or less, the signal's excess is −0.10 % (1765 cases).
- F4: The book's deepest falls came in rising markets. In w16 the coins rose +0.54 on average, while the book lost −0.18 and fell −44 %. It bought low-volume dips: the mean volume ratio on the days it held was 1.0–1.1, and five of the six coins lost between −0.13 and −0.30. In w24, with coins up +0.45, the book lost −0.05.
