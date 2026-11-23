---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4039 USD
---
## Findings
- **F1:** The book fails on Calmar (0.69 against 0.75 required) because its deepest falls came inside the coins' own bear markets: -25.8 % across w1–w3 while holding the coins fell -66 %, -25.5 % in w16 while holding fell -62 %, and -19.2 % across w12–w14 while holding fell -68 %.
- **F2:** The rebound exists only when volatility is elevated: on held bars, the next-day excess return is -0.36 % (t -2.79, n 1310) when the 20-day volatility is at or below 0.8 of its 120-day mean, +0.68 % (t 2.50, n 453) between 1.2 and 1.4, and +0.90 % (t 4.04, n 694) above 1.4. Signal bars with a ratio of at least 1.1 earn +0.59 % (t 3.99, n 1506), against -0.07 % (t -0.89, n 2872) below 1.1.
- **F3:** Elevated volatility is not an effect of its own: bars with a ratio of at least 1.1 and no signal earn -0.30 % the next day (t -2.27, n 1603), and in the top volatility tercile the no-signal bars earn -0.32 % (t -2.38) against +1.12 % (t 3.64, n 433) on the deepest-fall signals. The condition is part of the idea's own theory: the rebound grows with volatility.
- **F4:** Inside the top volatility tercile the effect is graded by the depth of the fall: +1.12 % (t 3.64) for the deepest third of falls, +0.50 % (t 1.99) for the middle third and +0.38 % (t 1.65) for the shallowest. In the bottom tercile every fall third loses, from -0.16 % to -0.30 %.
- **F5:** In a re-simulation (0.095 % per side, which reproduces Calmar 0.71 for the book as is), two changes raise Calmar above the bar:
- **F6:** The signal earns nothing when the coin's 20-day return is in its middle quartiles (+0.00 %, t 0.04; and -0.03 %, t -0.29). It pays after extreme 20-day moves: +0.25 % (t 1.95) in the lowest quartile and +0.52 % (t 3.86) in the highest. No-signal bars in the highest quartile earn +0.00 % (t 0.04), so the extreme move alone does not carry it.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound.d1_volatile-fall-rebound-squared` (from F1, F2, F3, F4, F5): The larger a coin's one-day fall, measured in its usual daily moves, the more it rises over the next day, only while its 20-day volatility stands above its own 120-day level. The rebound grows with the square of how far that volatility is elevated, so it is several times larger when volatility is most elevated than when it is barely above its norm.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound.d2_fall-rebound-after-extreme-runs` (from F6, F2): The larger a coin's one-day fall, measured in its usual daily moves and weighted by how high its 20-day volatility stands against its 120-day level, the more it rises over the next day, only after a large 20-day move in either direction. The rebound grows with the size of that 20-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
