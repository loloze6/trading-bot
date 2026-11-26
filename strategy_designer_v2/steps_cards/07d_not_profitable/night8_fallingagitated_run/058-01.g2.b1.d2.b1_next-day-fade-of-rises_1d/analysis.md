---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.b1.d2.b1_next-day-fade-of-rises_1d
idea tested: 058-01.g2.b1.d2.b1_next-day-fade-of-rises
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5728 USD
---
## Findings
- **F1:** The book loses on the largest rises, where it is shortest. Profile up days in the top quartile of the rise against the 30-day swing (z 0.79 to 4.49) carry the largest short (mean allocation -0.55, against -0.02 to -0.23 in the other quartiles), yet their next-day unusual move is only +0.11 % (t 0.19, 160 cases); 25 of the 30 worst case losses fall in that quartile, summing -1.54 against a total case gain of +0.63.
- **F2:** The fade lives in the middling rises. The third quartile of the rise (z 0.44 to 0.78) gives a next-day unusual move of +1.46 % (t 3.59, 159 cases); on the standardised forecast, the second-most-short quartile gives +1.66 % (t 4.33) while the most-short quartile gives -0.12 % (t -0.21).
- **F3:** An equal one-day short after a cost of 0.22 % earns +0.69 % per case on the three lower quartiles of the rise and -0.30 % on the top quartile (+0.45 % on all). The idea's total move covers its cost only without the largest rises.
- **F4:** The book's falls come from coins that kept rising. Its 15 worst days had a mean coin return of +5.95 % and summed to -27.2 %, against a log-sum of +8.3 % for the whole book. Its deepest falls were in w14 (-5.7 %) and w18 (-4.0 %), so the Calmar of 0.33 is set by the oversized shorts of F1. In 2021 the top quartile's unusual move was -2.39 % (33 cases) against +1.42 % for the rest (168 cases).
- **F5:** The horizon is one day. Over 3 days the unusual move shrinks to +0.20 % to +1.04 % with t at most 1.21, and an equal 3-day short nets -0.26 % after cost.
- **F6:** The effect belongs to the profile. Outside it, up days of every size quartile give a next-day unusual short move of only +0.03 % to +0.25 % (t at most 1.55), and +0.04 % against the short over 3 days.
- **F7:** Inside the decline, the middling rises of coins still far below their 20-day high fade more: +1.74 % (t 2.86, 88 cases) against +1.04 % (t 2.05, 72 cases) for those near it. The condition alone, on all profile days, earns the opposite way: -0.62 % for a short (t -2.52, 723 cases), and -1.87 % on its down days (t -5.75). So "far below the high" is not an effect of its own on the short side; it fits the theory's waiting supply of underwater holders. It does not help the top quartile (-0.30 %, t -0.47).
- **F8:** After a top-quartile rise followed by a down day, the coin rebounds on the next day: the short loses -1.98 % (t -3.22, 88 cases). After a top-quartile rise followed by another up day, the short gains +0.73 % (t 1.03, 72 cases). The largest rises behave like real demand, not a squeeze that fades at once.

## Ideas
- `058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day` (from F1, F2, F3, F4, F5, F6): In a falling, agitated market, a coin's one-day rise of middling size against the standard deviation of its daily returns over the past 30 days is the one most given back over the next day. The share given back grows with the rise up to about its usual swing and shrinks for the rarest, largest rises.
- `058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade` (from F2, F7, F1, F5): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day. The fall is larger still the further the coin's close stays below its 20-day high, for rises of up to about one usual swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
