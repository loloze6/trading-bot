---
line: 7.d confirmed, not profitable
backtest: 067-01.b1.g1.b1_choppy-month-fall-continues_1d
idea tested: 067-01.b1.g1.b1_choppy-month-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4645 USD
---
## Findings
- **F1:** The effect only appears after deep 30-day falls, and the shallow falls that the book also shorts lose. On choppy grid bars, the 10-day move after the coin's normal drift (negative means falling) was -6.4 % after a 30-day fall deeper than 20 % (t -2.09, n 38) and -9.0 % after a fall of 10 to 20 % (t -4.19, n 27). It was -0.3 % after a fall of 5 to 10 % (t -0.07, n 16) and +5.4 % after a fall of 0 to 5 % (t 1.66, n 25). In plain terms, coins that slid a little in a flat market bounced against the short.
- **F2:** Deep falls only carry this effect inside the choppy market, so depth is a stronger case of the idea's own situation and not an effect of its own. With the 60-day trend recomputed on the grid, the short-direction unusual 10-day move after a 30-day fall of over 20 % was +18.6 % in choppy markets (t 5.15, n 10), against -1.2 % in falling markets (t -0.72, n 124) and +8.9 % in rising markets (t 1.58, n 5). After a fall of 10 to 20 % it was +12.5 % in choppy markets (t 4.56, n 18), against +4.0 % in falling markets (t 1.85, n 56) and +2.3 % in rising markets (t 0.62, n 19).
- **F3:** The forecast is standardised against its own past 60 values, and this blurs the depth of the fall. By forecast size, the short-direction unusual move was +4.5 % for -21 to -10 (t 1.35, n 31), +7.0 % for -10 to -5 (t 2.50, n 37), +0.9 % for -5 to -2 (t 0.41, n 24) and -4.7 % for -2 to 0 (t -0.99, n 14). The raw-depth bands in F1 sort the cases far more cleanly than this.
- **F4:** The book loses because it fights the coins' upward drift on shallow cases and holds too briefly. Per case, the total move was -0.10 % against a cost of 0.22 %. Of the 535 short trades, those of 0 to 3 days lost 5.5 % net (n 114), 3 to 10 days lost 3.3 % (n 195) and 10 to 20 days lost 1.8 % (n 161). Only those of 20 to 40 days won, +7.5 % (n 58). Choppy shorts after a deep fall kept paying over 20 days: +18.9 % after a fall over 20 % and +11.5 % after a fall of 10 to 20 %.
- **F5:** The leave-one-window-out failure comes from windows in which the coins rose strongly. The book lost 10.5 % in w10 (holding +67 %), 5.8 % in w11 (holding +229 %), 6.9 % in w8 (holding +38 %) and 5.9 % in w17 (holding +39 %). Trades still short when the profile turned rising lost 22.7 % (n 48), and trades closed by the forecast returning to 0 lost 5.9 % and 7.8 % (n 61 and 82).
- **F6:** Among choppy shorts, those with low realised volatility did not work, while those with middle or high volatility did. The short-direction unusual move was -1.2 % in the low-volatility third (t -0.42, n 36), against +4.5 % in the middle third (t 1.97, n 34) and +4.4 % in the high third (t 1.41, n 36). This was not checked against the profile's own agitation measure and is not used for an idea.

## Ideas
- `067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues` (from F1, F2, F3, F5): In a choppy market, the larger a coin's plain percentage fall over the past 30 days, the more it keeps falling over the next 10 days, the continuation growing steeply with the depth of the slide so that the deepest slides carry most of the move.
- `067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days` (from F2, F4): In a choppy market, the larger a coin's fall over the past 30 days, the more it keeps falling over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
