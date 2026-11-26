---
line: 7.g patterns
backtest: 074-01.b1.d1_run-break-fade-widening-swing_1d
idea tested: 074-01.b1.d1_run-break-fade-widening-swing
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4655 USD
---
## Findings
- **F1:** In falling markets the next-day fade belongs to the up day that ends a down run, not to up days in general: run-ending up days were followed by a short-signed unusual move of +1.10 % in agitated markets (t 2.05, day-clustered, 356 cases on 128 days) and +1.22 % in calm ones (t 2.76, 200 cases on 107 days). Up days that follow an up day showed none: +0.05 % agitated (t 0.08, 253 cases) and −0.49 % calm (t −1.05, 164 cases).
- **F2:** The run-break fade is absent or reversed in rising markets, at −0.73 % agitated (t −1.47, 198 cases) and −0.06 % calm (t −0.14, 249 cases). In falling markets it grows only loosely with the run's length: +0.93 % after 1 down day (t 3.0, 281 cases), +1.52 % after 2 (t 3.7, 142), +0.32 % after 3 (t 0.6, 79), +2.40 % after 4 (t 2.4, 25) and +2.48 % after 5 or more (t 2.6, 29).
- **F3:** The mirror pattern also holds in falling markets. After the first down day that ends a run of up days, the next day's long-signed unusual move grows with the up run's length by +0.49 % per up day (t 3.14, 567 cases). There is no such slope in rising markets (−0.11 % per day, t −0.58, 449 cases). The agitated falling cases rise from +0.65 % after 1 up day (218 cases) to +1.69 % after 3 (36 cases) and +3.04 % after 4 or more (t 1.80, 28 cases on 18 days). The calm ones rise from −1.05 % after 1 to +1.40 % after 4 or more (24 cases).
- **F4:** Across all days of a falling agitated market, a larger move today in 30-day swings is followed by a larger opposite move the next day (slope −1.15 % per swing, t −7.4, 1264 days). In falling calm markets there is no such slope (+0.11 %, t 0.73, 799 days). This pattern is already held: 058-02.b1.g1.b1.b1, falling agitated next-day reversal. It is also concentrated in 2020 (slope −2.91 %, t −9.9), against −0.32 % (t −1.8) in 2018 and −0.03 % (t −0.1) in 2021.
- **F5:** The tested book's edge is fading over time. The per-case short-signed unusual move was +1.50 % in 2018 (t 5.2, 398 cases), +0.52 % in 2019 (t 2.4), +0.57 % in 2020 (t 1.5) and +0.32 % in 2021 (t 0.7). Of the book's windows, w14 carries the largest mean daily return, 0.24 % against roughly 0 to 0.14 % in the others, with the widest range (−6.5 % to +8.2 %). This fits the Calmar failure.
- **F6:** The calendar patterns do not stand out given how many angles were examined. The falling-market Saturday gain was +0.84 % (t 2.14, 62 days), but it reversed in 2020 at −1.50 % (t −1.2). The cases' weekday spread ran from −0.91 % on Tuesday to +2.34 % on Sunday, with no reason behind it.

## Ideas
- `074-01.b1.d1.g1_falling-market-rally-break-rebound` (from F3, F2): In a falling market, the first down day after a run of consecutive up days is followed by a rise in the coin's close over the next day. The more up days the run held, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
