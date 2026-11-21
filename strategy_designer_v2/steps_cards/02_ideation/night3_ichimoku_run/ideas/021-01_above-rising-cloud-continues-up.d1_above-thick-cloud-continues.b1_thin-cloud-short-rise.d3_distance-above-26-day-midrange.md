---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 5 days is larger the further its close stands above the midpoint of its past 26 days' high-low range.
Consequence: A trader would hold a coin in proportion to how far it trades above its recent equilibrium, including the many days when it is not above a rising cloud.
Why:
- F1: The book fails on its mean daily return (0.000459 against the 0.0005 required), while holding the coins earns 0.00118 a day; the book holds a position on only 28 % of bars, at a mean allocation of 0.54 when in (0.15 over all bars), so it is out of the coin most of the time. Its gain per bar splits into 0.000179 from the market's own rise and 0.000301 from timing.
- F6: Outside the regime (72 % of bars) the coin still rises 0.078 % a day before removing its drift. Its 5-day excess return is graded by the close's distance to the 26-day midpoint, from -0.33 % in the lowest quintile (mean -24.5 %) to +0.39 % in the highest (mean +11.3 %), with raw 5-day returns of 0.27 % to 1.00 % (about 404 cases each).
- F7: Leaving the regime is not followed by a fall: the 5-day excess return after an exit is +0.49 % (t 0.72, 293 cases), and the 10-day return is +1.07 %.
