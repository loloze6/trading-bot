---
line: 7.g patterns
backtest: 075-01_heavy-volume-next-day-rise_1d
idea tested: 075-01_heavy-volume-next-day-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3766 USD
---
## Findings
- **F1:** The book's whole gain comes from the heaviest-volume fifth of days. The position's next-day gain is +0.522 % per coin-day there (t 5.27, 2267 cases), against −0.025 % to +0.033 % in the other four fifths (|t| ≤ 1.6). The idea's graded slope adds nothing between light and ordinary volume.
- **F2:** The heavy-volume lean lives on down days. After a down day in its coin's top volume fifth, the next-day excess return is +1.18 % (t 5.33, 1049 cases). The other down-day volume fifths give −0.22 % to +0.39 % (t ≤ 2.0). After up days in the top fifth it is −0.001 % (t 0.00, 1218 cases).
- **F3:** Inside heavy-volume days the rebound grows with the size of the fall. In the coin's largest-fall fifth of days with top-fifth volume, the next-day excess is +1.40 % (t 5.01, 728 cases). In the second-largest-fall fifth it is +0.93 % (t 2.32, 252). On flat-to-rising days with heavy volume it is −0.36 % to +0.26 % (|t| < 1).
- **F4:** Heavy-volume days that close near their low rebound most. They return +1.33 % next day (t 4.91, 641 cases), against +0.69 % for mid closes (t 2.47) and −0.12 % for high closes (t −0.46).
- **F5:** Up days on light-to-ordinary volume drift lower the next day. The bottom three volume fifths give −0.39 %, −0.58 % and −0.61 % (t −2.64, −3.71, −3.85; about 1130 cases each). The top fifth gives 0.00 %. The fall is not graded at the light end, and these t's are not clustered by day.
- **F6:** The heavy-volume rebound is not confined to one trend. On the coin's 20-day trend, the top volume fifth gives +0.61 % when falling (t 1.89), +0.37 % when choppy (t 1.83) and +0.45 % when rising (t 1.67).
- **F7:** The per-case move on heavy-volume down days covers the cost of a trade, unlike the tested idea. Heavy down days give +1.18 % per case against a 0.22 % trade cost, about 5 times the cost. The tested idea's total move is +0.07 % per case, 0.3 times the cost. On the 3-day grid the heavy down days give +1.52 % (t 2.33, 330 cases).

## Ideas
- `075-01.g1_heavy-volume-down-day-rebound` (from F1, F2, F3, F4, F6, F7): On a day a coin falls, the heavier its volume against its own average daily volume over the past 20 days, the larger its rise over the next day, in any market.
- `075-01.g2_light-volume-up-day-fade` (from F5): On a day a coin rises, the lighter its volume against its own average daily volume over the past 20 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
