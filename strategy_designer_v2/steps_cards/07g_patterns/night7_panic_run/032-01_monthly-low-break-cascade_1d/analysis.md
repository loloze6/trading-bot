---
line: 7.g patterns
backtest: 032-01_monthly-low-break-cascade_1d
idea tested: 032-01_monthly-low-break-cascade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3921 USD
---
## Findings
- **F1:** The tested cascade runs the other way: on the active bars (falling agitated profile, close below the prior 30-day closing low), the coin's 3-day return above its normal drift averages +3.77 % (t 1.93, 38 cases on 19 days). Over all folds, step 5 measured the short-side unusual move at -2.20 % (t -1.98, 163 cases on 86 days). Together this points to a rebound, not a further fall.
- **F2:** The rebound in that profile builds over the 3 days. The unusual move is +0.58 % after 1 day (t 0.36), +1.58 % after 2 days (t 0.92), +3.77 % after 3 days (t 1.93) and +4.13 % after 5 days (t 1.14), all on the same 38 cases.
- **F3:** The depth of the break below the 30-day low does not grade the move. Among falling-market breaks, the slope of the 3-day unusual move on depth has t 0.46 (73 cases). The quartiles are not monotone: deepest +1.44 %, q2 +2.13 %, q3 -0.76 %, shallow -1.16 %, all with |t| ≤ 1.06.
- **F4:** Breaks that close in the top third of the day's range are followed by +4.86 % over 3 days (t 1.26, 12 cases on 8 days). Breaks closing low or mid-range show about 0 % (-0.08 % and -0.11 %). The slope on close location among falling-market breaks has t 1.17. This is suggestive only.
- **F5:** In a rising market (60-day return above +10 %), a down day of 1 to 2 daily swings is followed by an unusual 3-day move of +7.18 % (t 2.97, 49 cases on 21 days) and an unusual 2-day move of +3.39 % (t 2.66). A down day beyond 2 swings gives +2.40 % (t 2.49, 7 cases on 6 days). Down days in falling or choppy markets show no such rebound (-1.48 %, t -0.71).
- **F6:** In a falling market, an up day larger than one daily swing is followed by an unusual 3-day move of -3.74 % (t -2.11, 64 cases on 26 days). In a choppy market the same up day gives -2.10 % (t -2.36, 32 cases on 22 days). In a rising market it gives +1.31 % (t 0.93).
- **F7:** The book's 138 short trades lasted 12.4 days on average, far beyond the 3-day horizon, and won 29 % of the time. Their mean net result was -7.68 % (median -3.93 %), negative on every coin. Over the 3 days the move was 13 times the 0.19 % cost of a trade, so the losses come from the wrong side and the long holds, not from cost.

## Ideas
- `032-01.g1_monthly-low-exhaustion-rebound` (from F1, F2, F3, F7): In a falling, agitated market, when a coin closes below the lowest close of its previous 30 days, it rebounds over the next 3 days, and the further the close sits below that prior 30-day low, the larger the rebound.
- `032-01.g2_monthly-low-closing-off-lows` (from F1, F4): In a falling, agitated market, when a coin closes below the lowest close of its previous 30 days, it rebounds over the next 3 days, and the higher that close sits within the day's high-low range, the larger the rebound.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-01.g3_rising-market-dip-rebound` (from F5): In a rising market, after a down day, the coin rises over the next 3 days, and the larger that day's fall measured in its 30-day daily swing, the larger the rise.
- `032-01.g4_falling-market-rally-fade` (from F6): In a falling market, after an up day, the coin falls over the next 3 days, and the larger that day's rise measured in its 30-day daily swing, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
