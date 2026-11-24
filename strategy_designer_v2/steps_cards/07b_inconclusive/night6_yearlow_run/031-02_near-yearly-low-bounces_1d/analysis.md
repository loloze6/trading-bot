---
line: 7.b inconclusive
backtest: 031-02_near-yearly-low-bounces_1d
idea tested: 031-02_near-yearly-low-bounces
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3411 USD
---
## Findings
- **F1:** The test's slope is on the opposite side to the idea: the slope t is -1.70 at 20 days (806 cases), and it is negative at every horizon tried (-2.07 at 5 days with 3326 cases, -2.43 at 10 days with 1646 cases, -0.53 at 40 days, -0.41 at 60 days), so no horizon shows a bounce.
- **F2:** The negative slope comes from the top fifth of the forecast alone. At 20 days its mean excess return is -4.88 % (t -3.17, 161 cases). The other four fifths range from -0.10 % to +3.93 %, with no order among them.
- **F3:** The top fifth's fall is uncertain. With the cases of one day taken together, its t is only -1.75 (69 days) at 20 days and -1.35 (143 days) at 10 days, so the data cannot tell it reliably from zero.
- **F4:** Raw closeness to the yearly low, before standardising, predicts nothing: its slope t is -1.08 at 20 days and +1.22 at 10 days. Cases within 5 % of the low have a 20-day excess return of -4.4 % with t -1.06 on 40 cases. Whatever effect exists comes from the close being nearer the low than it usually is over the coin's past year, which is what the standardised forecast measures.
- **F5:** The top fifth's fall depends on the year:
- **F6:** The fall is concentrated where the coin's 60-day return is positive, which suggests a recovery that fails while price is still near its yearly low:
- **F7:** The fall is seen in five of the six coins. The top fifth's 20-day excess is between -2.9 % and -7.6 % for every coin. Per-coin slopes are negative with t between -0.29 and -1.68, except ZEC at +0.02.

## Ideas
- `031-02.b1_failed-rally-near-yearly-low` (from F1, F2, F4, F6, F7): The closer a coin's daily close is to its lowest close of the past 365 days, compared with how close it has usually been over that year, the more it falls over the next 20 days, while its 60-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
