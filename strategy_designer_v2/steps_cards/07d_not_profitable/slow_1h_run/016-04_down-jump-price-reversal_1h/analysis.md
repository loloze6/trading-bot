---
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal_1h
idea tested: 016-04_down-jump-price-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3041 USD
---
## Findings
- **F1:** Fees, not forecast errors, are what sink the book: it pays 0.0016 to 0.0024 of its value per day in fees on every coin (BTC 0.00172, XMR 0.00242), against a gross gain before fees of only -0.00043 to +0.00068 per day, which leaves a mean daily book return of -0.00187 against a required 0.0005.
- **F2:** The fees come from hourly churn: the position changes on about 12 bars per day on every coin (11.6 to 12.5), with a median change of only 0.027 to 0.040 of the book, because the forecast is restandardised over its last 73 hourly values while the 3-day fall it describes changes slowly.
- **F3:** Even before fees there is almost nothing to harvest: the forecast was positive on every active bar (no short side), and the strongest bucket (forecast above 5, n=1898 fallen grid cases) had a mean excess 72-bar return of -0.0031 (t -1.69), the opposite sign to the idea.
- **F4:** The top-3-losses share is mostly an inverse of the fall's size (correlation of log share with log fall size -0.90), so a high share mostly marks a small fall: the top share quintile had excess 72-bar return -0.0105 (t -2.95, n=534) against +0.0009 in the bottom quintile.
- **F5:** The size of the 3-day fall grades what follows the other way round from the forecast: the biggest-fall quintile (falls of 8.7% to 51%) won back +0.0060 in excess over the next 72 bars, while the smallest-fall quintile (falls under 1.3%) lost a further -0.0115 (n=533 to 534 each).
- **F6:** Among the biggest third of falls, the falls least concentrated in their 3 worst hours won back the most, +0.0156 excess over the next 72 bars, against -0.0009 and -0.0002 for the more jump-made ones; in the smallest third of falls every share tercile kept falling (-0.0120, -0.0043, -0.0091).
- **F7:** Falls built from choppy hours (lowest net-fall-to-total-hourly-movement quintile) kept falling, with excess -0.0087 (t -2.39, n=534), while the middle quintile rose +0.0035.

## Ideas
- `016-04_down-jump-price-reversal.d1_deep-falls-revert-shallow-continue` (from F4, F5, F3): The larger a coin's fall over the past 3 days, the more of that fall it wins back over the next 3 days, and the smaller the fall, the more the coin keeps drifting lower over those 3 days.
- `016-04_down-jump-price-reversal.d2_large-grinding-falls-revert` (from F6, F5, F4): When a coin has fallen over the past 3 days, the larger the share of that fall that came from its few biggest hourly losses, the more of the fall the coin wins back over the next 3 days, except that among large 3-day falls the more evenly the fall was spread across the hours, the more the coin wins back over the next 3 days.
- `016-04_down-jump-price-reversal.d3_choppy-falls-keep-falling` (from F7, F3): The more a coin's 3-day fall came from choppy hours, with much hourly movement in both directions for little net decline, the further the coin falls over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
