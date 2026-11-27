---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d2_quiet-high-close-fades_1d
idea tested: 061-01.b1.b1.b1.d2_quiet-high-close-fades
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4590 USD
---
## Findings
- **F1:** The fade in the profile grows with the holding period and is about twice as large at ten days as at five. After a high close (top 20 % of the range) on a small up day, the unusual move in the short's direction is +2.9 % at 3 days (t 1.53, 38 cases), +4.9 % at 5 days (t 3.19, 35 cases), +5.7 % at 7 days (t 2.96), +9.6 % at 10 days (t 4.28, 30 cases on 28 days, strength 0.53, 63 % of cases fall) and +11.2 % at 15 days (t 4.04, 28 cases). A five-day hold therefore captures about half of the move, which keeps the yearly return (+0.6 %) small against the deepest fall (0.8 %) and holds Calmar at 0.595.
- **F2:** The book trades too little (0.006 trades per day, against 0.01 required) because the signal is rare: only 4.6 % of bars are in the profile, and only 35 five-day grid cells hold a case. Widening the close from "top 20 %" to "upper 40 %" of the range keeps the effect and raises the cases by about 1.7 times. At 5 days that is 60 cases, +3.8 %, t 2.59; at 10 days it is 49 cases, +5.9 %, t 3.05. A close above the middle gives 53 cases, +5.9 %, t 3.10 at 10 days.
- **F3:** Inside the profile, the fade is graded by where the close sits in the day's range. On small up days, the 10-day unusual move is +9.6 % for a close in 0.8–1.0 of the range (t 4.28, 30 cases), +3.2 % for 0.6–0.8 (t 1.30, 31 cases), +0.3 % for 0.4–0.6 (20 cases) and −5.2 % for 0.0–0.4 (6 cases). The nearer the close to the high, the larger the fall.
- **F4:** The profile is not an effect of its own, and the agitation is what carries the fade. Profile bars without the signal move only +1.2 % at 10 days (t 0.65, 127 cases) and +0.5 % at 5 days (t 0.39). The same signal in a choppy but calm market moves +1.7 % at 10 days (t 0.76, 71 cases). Outside the profile the signal moves +0.5 % at 5 days (t 0.75, 570 cases), and in rising markets −0.6 % (t −0.41).
- **F5:** At five days the fade is graded by the size of the day's gain, as the tested idea says, and large up days do not fade. For a high close in the profile, the 5-day unusual move is +6.8 % for gains of 0–0.33 usual moves, +5.9 % for 0.33–0.66, +3.3 % for 0.66–1, +1.9 % for 1–2 (t 0.82) and +2.4 % for gains above 2. At ten days, with the wider close of F2, the gain bins are not ordered: +8.8 %, +5.1 % and +7.2 %.
- **F6:** The effect points the same way in every year of folds B and C. With the wider close at 10 days, the mean unusual move is +18.4 % in 2018 (4 cases), +5.8 % in 2019 (12), +5.3 % in 2020 (10) and +4.1 % in 2021 (23). It is positive on all nine coins with cases, though small on BTC (+0.5 %, 6 cases) and XMR (+1.4 %, 7 cases).
- **F7:** The book's falls are small and spread out rather than one event. The deepest fall is 0.8 %, and the worst day is −0.5 %. Six windows end below +0.25 %: w14, w7, w8 and w9 hold no position, while w10 and w12 lose slightly. The book is short on only 1.5 % of bars, at a mean allocation of 0.15. The weak Calmar comes from too little gain per fall, which a longer hold (F1) addresses, not from a crash to avoid.

## Ideas
- `061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade` (from F1, F3, F4, F7): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range on a day whose gain is small against its usual daily swing, its price falls over the next ten days, and the nearer the close is to the day's high, the larger the fall.
- `061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade` (from F2, F3, F4, F6): In a choppy, agitated market, when a coin closes in the upper part of that day's high-low range on a day whose gain is small against its usual daily swing, its price falls over the next ten days, and the higher the close sits in the day's range, the larger the fall.
- `061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade` (from F5, F4, F2): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range on an up day, its price falls over the next five days, and the smaller the day's gain against its usual daily swing, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
