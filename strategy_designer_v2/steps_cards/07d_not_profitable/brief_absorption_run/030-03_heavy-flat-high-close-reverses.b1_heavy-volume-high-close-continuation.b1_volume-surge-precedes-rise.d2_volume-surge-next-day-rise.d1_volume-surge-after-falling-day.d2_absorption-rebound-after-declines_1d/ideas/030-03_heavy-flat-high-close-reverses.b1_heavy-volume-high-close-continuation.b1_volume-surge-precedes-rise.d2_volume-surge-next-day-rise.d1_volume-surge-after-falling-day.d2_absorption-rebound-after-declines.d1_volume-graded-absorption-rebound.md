---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a down day relative to its own prior 20-day average, the more the coin rises over the next day, and the rebound grows steeply with that volume multiple, so that a fall on volume several times its usual level is followed by a far larger next-day rise than an ordinary-volume fall in the same 20-day decline.
Consequence: A trader takes the next-day long after a 20-day decline's down day in proportion to the day's volume multiple, keeping out on ordinary-volume falls whose rebound does not cover a trade's cost.
Why:
- F1: The book's gain comes from the heavy-volume part of the signal; on low-volume falls the edge is smaller than one trade's cost. Held bars after a volume ratio of 1.5–2.5 earned +0.64 % per bar (466 bars), and after a ratio above 2.5 they earned +0.94 % (194 bars). After a ratio of 1 or less they earned only +0.11 % (2210 bars, more than half of all held bars), and from 1 to 1.5 they earned +0.06 % (700 bars). One trade costs 0.19 %.
- F2: Restricting the same one-day long to signal days with volume above 1.5 times its 20-day average fixes both failing measures in a simple simulation. The deepest fall drops from −47.8 % to −11.6 %, Calmar rises from 0.23 to 0.69, and Sharpe rises from 0.52 to 0.71, while the position is held on 3.6 % of coin-days instead of 24.6 %. Raising the forecast threshold instead (forecast ≥ 15) leaves Calmar at 0.21 and the fall at −45.6 %, because the forecast's size is driven by the fall and the prior decline, not by volume.
- F4: The book's deepest falls came in rising markets. In w16 the coins rose +0.54 on average, while the book lost −0.18 and fell −44 %. It bought low-volume dips: the mean volume ratio on the days it held was 1.0–1.1, and five of the six coins lost between −0.13 and −0.30. In w24, with coins up +0.45, the book lost −0.05.
