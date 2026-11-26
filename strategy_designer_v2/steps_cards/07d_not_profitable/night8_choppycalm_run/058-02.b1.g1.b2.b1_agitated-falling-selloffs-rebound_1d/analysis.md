---
line: 7.d confirmed, not profitable
backtest: 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d
idea tested: 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4011 USD
---
## Findings
- **F1:** The check failed on the falls only: Calmar is 0.676 against the 0.75 rule, with Sharpe 0.99 and a mean of 0.22 % a day in a position, and the deepest fall (−5.7 % in w14, over 15 days) comes from a few big losing days. Its three worst days make 118 % of that fall, and its single worst day is −4.8 %; the next falls are −3.9 % in w9, spread over 69 days, and −2.2 % in w13.
- **F2:** The smallest falls carry none of the effect but still carry risk. Split into quarters by forecast (675 signal bars, folds B and C), the bottom quarter's mean unusual next-day move is −0.13 % (t −0.27). The other three quarters show +1.75 % (t 4.22), +0.95 % (t 2.78) and +2.45 % (t 4.28).
- **F3:** A fall that is the second down day in a row carries the effect best against its losses. On 280 such cases the unusual next-day move is +1.73 % (t 4.72), with a mean position gain of +0.86 % against a 5th-percentile loss of −1.38 %. On the 395 cases after an up day it is +0.92 % (t 3.05), with a gain of +0.30 % against a 5th-percentile loss of −1.84 %. This condition was not measured on bars without the signal.
- **F4:** The effect grows with how far the coin had already slid. Signals in the deepest third of the prior 5-day return show +2.21 % (t 4.43), the middle third +0.35 % (t 1.22) and the top third +1.23 % (t 2.91). By the 20-day return, the deepest third shows +2.16 % (t 4.20) and the shallowest +0.65 % (t 1.61). This condition was not measured on bars without the signal.
- **F5:** A fall that closes near the day's low rebounds most, and the condition is not an effect of its own. Signals closing in the bottom fifth of the day's range show +2.08 % (t 4.69), against +0.92 % mid-range and +0.51 % (t 0.77) in the upper half. In-profile bars without the signal that close mid-range or high show −1.25 % (n 101) and −0.94 % (n 514), and only 8 such bars close at the low.
- **F6:** The largest positions are also where the deepest losses sit. In the top forecast quarter the worst position-day is −9.1 % and the 5th percentile −3.95 %, against −1.10 % in the second quarter.
- **F7:** The size is not the problem. The total move per case is +1.18 %, 6.1 times the 0.19 % cost of a trade, and 0.225 of a usual move.

## Ideas
- `058-02.b1.g1.b2.b1.d1_second-day-selloff-rebound` (from F1, F3, F2): In a falling, agitated market, the larger a coin's one-day fall against its usual daily swing over the last 20 days, when it is its second down day in a row, the larger its rise over the next day.
- `058-02.b1.g1.b2.b1.d2_low-close-selloff-rebound` (from F5, F1, F2): In a falling, agitated market, the larger a coin's one-day fall against its usual daily swing over the last 20 days and the nearer that day's close to its low, the larger its rise over the next day.
- `058-02.b1.g1.b2.b1.d3_capitulation-after-slide-rebounds` (from F4, F2, F1): In a falling, agitated market, the larger a coin's one-day fall against its usual daily swing over the last 20 days, coming on top of a fall over its previous 5 days, the larger its rise over the next day, growing with the depth of both.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
