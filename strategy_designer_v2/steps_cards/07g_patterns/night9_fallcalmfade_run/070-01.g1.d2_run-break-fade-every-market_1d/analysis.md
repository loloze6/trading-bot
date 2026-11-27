---
line: 7.g patterns
backtest: 070-01.g1.d2_run-break-fade-every-market_1d
idea tested: 070-01.g1.d2_run-break-fade-every-market
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2672 USD
---
## Findings
- **F1:** The fade grows with the horizon and with the run's length: over the next 3 days the short-direction unusual move after an up day that breaks a down run is +0.14 % after 1 down day (t 0.34, 1268 cases, 465 days), +1.11 % after 2 (t 1.61, 569 cases), +1.27 % after 3 (t 1.71, 288 cases), +1.71 % after 4 (t 1.53, 101 cases) and +3.25 % after 5 or more (t 3.04, 79 cases, 56 days). Over 1 day the same groups give +0.22 %, +1.08 %, +0.80 %, +0.51 % and +2.21 %. The 3-day move per case is 6 to 17 times the 0.19 % cost of a trade, against 3 times for the 1-day move.
- **F2:** The 1-day fade after runs of 2 or more down days depends on the 60-day trend. It is +1.57 % in falling calm (t 2.75, 117 cases, 65 days), +1.20 % in falling agitated (t 1.59, 158 cases), +1.26 % in choppy calm (t 1.49, 56 cases) and +0.92 % in choppy agitated (t 0.86, 26 cases). In rising markets it is gone or reversed: +0.25 % in rising agitated (t 0.37, 85 cases) and −1.02 % in rising calm (t −1.59, 91 cases).
- **F3:** After a single down day the break is not followed by a fall in any size bucket: +0.41 %, +0.35 %, +0.42 % and −0.18 % from the smallest to the largest up-day quartile, all with |t| < 1.3. After runs of 2 or more, the fade holds at +0.73 % to +1.01 % whatever the up day's size.
- **F4:** The fade is absent when the breaking up day closes in the bottom third of its range: +0.15 % (t 0.10, 46 cases). It holds when the day closes in the middle third (+1.05 %, t 2.29, 299 cases) and in the top third (+1.09 %, t 3.47, 703 cases).
- **F5:** Other angles show nothing new or nothing that stands out after this many looks.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `070-01.g1.d2.g1_run-break-three-day-fade` (from F1, F3): An up day that ends a run of down days is followed by a fall over the next three days. The fall is larger the more down days the run held, and close to nothing after a single down day.
- `070-01.g1.d2.g2_falling-market-run-break-fade` (from F2, F3): In a falling market, an up day that ends a run of down days is followed by a fall over the next day. The fall is larger the more down days that run held beyond the first.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
