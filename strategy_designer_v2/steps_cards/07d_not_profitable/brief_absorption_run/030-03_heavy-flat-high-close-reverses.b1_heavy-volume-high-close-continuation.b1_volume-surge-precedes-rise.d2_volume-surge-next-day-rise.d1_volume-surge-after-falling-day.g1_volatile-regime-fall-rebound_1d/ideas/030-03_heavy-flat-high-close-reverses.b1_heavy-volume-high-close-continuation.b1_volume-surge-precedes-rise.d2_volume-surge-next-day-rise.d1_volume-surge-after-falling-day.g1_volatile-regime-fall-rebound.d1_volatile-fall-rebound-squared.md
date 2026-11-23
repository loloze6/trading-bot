---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured in its usual daily moves, the more it rises over the next day, only while its 20-day volatility stands above its own 120-day level. The rebound grows with the square of how far that volatility is elevated, so it is several times larger when volatility is most elevated than when it is barely above its norm.
Consequence: A trader buys a sharp daily fall in proportion to the fall times the square of the volatility ratio, and holds little or nothing in calm periods, where the same fall loses.
Why:
- F1: The book fails on Calmar (0.69 against 0.75 required) because its deepest falls came inside the coins' own bear markets: -25.8 % across w1–w3 while holding the coins fell -66 %, -25.5 % in w16 while holding fell -62 %, and -19.2 % across w12–w14 while holding fell -68 %.
- F2: The rebound exists only when volatility is elevated: on held bars, the next-day excess return is -0.36 % (t -2.79, n 1310) when the 20-day volatility is at or below 0.8 of its 120-day mean, +0.68 % (t 2.50, n 453) between 1.2 and 1.4, and +0.90 % (t 4.04, n 694) above 1.4. Signal bars with a ratio of at least 1.1 earn +0.59 % (t 3.99, n 1506), against -0.07 % (t -0.89, n 2872) below 1.1.
- F3: Elevated volatility is not an effect of its own: bars with a ratio of at least 1.1 and no signal earn -0.30 % the next day (t -2.27, n 1603), and in the top volatility tercile the no-signal bars earn -0.32 % (t -2.38) against +1.12 % (t 3.64, n 433) on the deepest-fall signals. The condition is part of the idea's own theory: the rebound grows with volatility.
- F4: Inside the top volatility tercile the effect is graded by the depth of the fall: +1.12 % (t 3.64) for the deepest third of falls, +0.50 % (t 1.99) for the middle third and +0.38 % (t 1.65) for the shallowest. In the bottom tercile every fall third loses, from -0.16 % to -0.30 %.
- F5: In a re-simulation (0.095 % per side, which reproduces Calmar 0.71 for the book as is), two changes raise Calmar above the bar:
