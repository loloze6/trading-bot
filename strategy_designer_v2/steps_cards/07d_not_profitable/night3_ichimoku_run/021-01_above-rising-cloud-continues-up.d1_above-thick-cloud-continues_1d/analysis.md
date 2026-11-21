---
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
idea tested: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.6418 USD
---
## Findings
- **F1:** The book's gain fails mainly because it is barely invested. It is in the market on 44 % of bars, at a mean allocation of 0.51 when in. It earns 3.45 bps a day against the coins' 11.9 bps. Of those 3.45 bps, 2.60 come from the market's own rise and only 0.83 from timing, so it trails holding on Sharpe (-0.046) and on mean daily return.
- **F2:** The cloud-thickness forecast works the wrong way round. On held days, the thickest third of forecasts (10.6 to 20) is followed by -16.2 bps a day relative to the coin, against +12.1 to +13.1 bps for the thinner ones. On the 26-day grid inside the regime, the thinnest third is followed by +11.3 % (t 1.21, n 50), against +0.2 % and +2.9 % for the thicker thirds. This is why the main slope is negative (t -1.26, 149 cases).
- **F3:** Inside the same held situation, how far the close stands above its 26-day average does grade what follows. Held days in the top fifth (more than 11.6 % above) are followed by +42.5 bps a day relative to the coin and gain the book 25.3 bps, against -15.2 to +14.1 bps for the other fifths. On the regime's 26-day grid, the top third gains +22.2 % (t 1.76, n 36), against -2.0 % for the bottom third (t -0.41, n 36).
- **F4:** On all 26-day grid bars, regime or not, the coin's past 26-day return grades its next 26-day excess return: slope 0.17, t 3.0, 432 cases.
- **F5:** The book's falls come in windows w16 to w21, where the chained book reaches its deepest fall of 47.5 %; its worst 30 days lose 27.6 % (w16). In w16 to w20 the coins rose 8 to 33 bps a day, yet the book lost on 5 of 6 coins (ZEC -14.1, XRP -8.9, LTC -7.8 bps a day).
- **F6:** Held days on which the close is below its 26-day average gain the book only 0.7 to 2.9 bps (coin 7.9 to 11.3 bps). Held days above it gain 12.8 to 14.4 bps (coin 33.0 to 46.1 bps).
- **F7:** Cost is not the cause. The idea's unusual move is +3.25 % per case over 26 days, 16.8 times the 0.19 % round trip. Flat days are followed by -5.6 bps a day relative to the coin, so being out is not itself what loses.

## Ideas
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d1_above-cloud-stretched-above-average` (from F2, F3, F6, F1): When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the further its close stands above its 26-day average price, rather than the thicker the cloud.
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d2_above-thin-cloud-continues` (from F2, F7): When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the thinner the cloud (the gap between its two spans as a share of the price).
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d3_26-day-momentum-continues` (from F4, F1, F5): A coin's return over the next 26 days is larger the higher its own 26-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
