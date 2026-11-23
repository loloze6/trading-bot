---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3735 USD
---
## Findings
- **F1:** The next-day rebound after a fall depends almost entirely on whether volatility is rising. Here a fall means a day below −1 usual move, scaled by the prior 20-day volatility. The ratio used is 20-day over 120-day volatility, past-only, split into terciles. In the top tercile of that ratio the coin's next-day excess return is +1.47 % (t 4.42, 335 cases). In the middle tercile it is +0.28 % (t 0.98, 349). In the bottom tercile it is −0.15 % (t −0.68, 442).
- **F2:** In a regression of the next-day excess return on all 17 480 days, the interaction of fall depth with the volatility ratio is the strongest term. It scores −0.37 % per standard deviation with t −7.14. The fall depth alone scores t −2.43, the close location t −1.85 and the volume t 2.01.
- **F3:** When volatility is rising (top tercile of the ratio), deeper falls are followed by larger rises. Falls of −1 to −1.5 usual moves give +0.79 % (t 2.01, 162 cases), falls of −1.5 to −2 give +1.99 % (t 3.80, 84), and falls beyond −2 give +2.23 % (t 2.48, 89). In the bottom tercile the same depths give +0.28 %, −0.69 % and −0.40 %, with no grading.
- **F4:** The rising-volatility rebound holds across the sample. It is positive in all 8 years (+0.19 % to +3.54 %) and in all 6 coins (BTC +1.51 % t 3.18, XRP +3.50 % t 3.30, the others +0.90 % to +1.41 %). Its mean, +1.47 % per case, is about 7.7 times the 0.19 % cost of a trade. The tested idea's unusual move is +0.19 %, only 1.0 times that cost.
- **F5:** The same split shows on the level of volatility within each coin. Falls below −1 usual move in the top tercile of the coin's own 20-day volatility are followed by +1.79 % (t 5.95, 607 cases). In the middle tercile the figure is +0.48 % (t 2.55, 679), and in the bottom tercile −0.20 % (t −1.39, 736).
- **F6:** Among falls below −1 usual move, a lower close in the day's range goes with a larger next-day rise: +0.91 % (t 4.17), +0.69 % (t 3.43) and +0.26 % (t 1.18) by close-location tercile, 674 cases each. This is the brief's absorption angle, but its spread is too small to stand out from the many angles examined.
- **F7:** The brief's own setup is heavy-volume, flat days (|z| < 0.5, top volume tercile). On those days the close location shows no link to the next day. The quintiles run from −0.76 % (t −1.47) to +0.31 % (t 0.85) with no order. The heavy-volume, low-close gain (+0.87 %, t 5.14) disappears outside falls (+0.20 %, t 1.09).
- **F8:** Weekday effects reverse between the two halves of the sample. Wednesday is −0.70 % (t −2.69) before 2022 and +0.10 % after; Thursday is +0.37 % before and −0.32 % after. They are not a pattern.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound.g1_rising-volatility-fall-rebound` (from F1, F2, F3, F4, F5): The larger a coin's one-day fall in units of its 20-day daily volatility, the more the coin rises over the next day. The higher its 20-day volatility stands against its 120-day volatility, the larger that rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
