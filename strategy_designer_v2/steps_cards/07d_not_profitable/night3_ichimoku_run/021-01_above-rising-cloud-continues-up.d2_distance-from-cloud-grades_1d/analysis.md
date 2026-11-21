---
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
idea tested: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3556 USD
---
## Findings
- **F1:** The book loses on its shorts and earns on its longs. Its 1953 short trades lost a mean -8.68 % net, held about 31 days each, while its 1017 long trades earned +14.89 % net. Bar by bar, short positions lost -6.8 bps per day while the coins rose +12.2 bps per day, and long positions earned +11.3 bps per day.
- **F2:** Below the cloud, the coin still rises; it only rises less than usual. On the 26-day grid, the 349 cases below the cloud top returned +1.77 % (-2.42 % against drift), and the 227 cases above it returned +7.68 % (+3.72 % against drift). Shorting the below side bets against a rise, which is why the total move per case is -0.65 % (-3.4 times the 0.19 % cost) even though the unusual move is +0.22 %.
- **F3:** The information is in which side of the cloud the close is on, not in how far from it. Within the above side, the slope of excess return on the forecast is flat (t -0.01, 227 cases). Within the below side it is slightly the wrong way (t -1.16, 349 cases).
- **F4:** By quintile of raw distance from the cloud top, excess returns jump at the top of the cloud and fade far from it. The five quintiles (-36 %, -17 %, -5 %, +6 %, +49 %) returned -3.9 %, -0.8 %, -2.6 %, +5.3 % and +2.0 % against drift. The best cases sit just above the cloud, not farthest above it.
- **F5:** Above the cloud with a rising 52-day trend, the coin returned +9.6 % over 26 days (116 cases). Below the cloud with a falling 52-day trend, it still returned +2.6 % (141 cases). Only the 27 cases below the cloud with a rising 52-day trend fell (-1.9 %).
- **F6:** The shorts are what cost the book across windows. In windows where the coins rose, the book lost: w16 -46 % summed against the coins' +54 %, w20 -24 % against +13 %, w23 -16 % against +32 %. Summed bar gains of the short side were negative on 4 of 6 coins, with XRP worst (-4.84), and XRP's long side also lost (-1.23).

## Ideas
- `021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades.d1_just-above-the-cloud` (from F1, F2, F3, F4): A coin's return over the next 26 days is larger the nearer above the top of its Ichimoku cloud its daily close stands, only while the close stands above the cloud top.
- `021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades.d2_fresh-cross-above-cloud` (from F2, F4, F5): A coin's return over the next 26 days is larger the fewer days have passed since its daily close crossed above the top of its Ichimoku cloud.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
