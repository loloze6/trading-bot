---
line: 7.g patterns
backtest: 033-01_close-near-low-rebounds_1d
idea tested: 033-01_close-near-low-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4043 USD
---
## Findings
- **F1:** The close's position within the day's range is graded against the next day's excess return. By quintile of close location, from low to high, the means are +0.52 % (t 3.82), +0.28 % (t 1.99), -0.25 % (t -1.95), -0.21 % (t -1.60) and -0.34 % (t -2.57), with about 1,740 cases each. The sign holds on all six coins, with t from 0.75 (XRP) to 4.83 (XMR), and in all four years, with t from 0.84 to 2.40.
- **F2:** The effect lives on wide days. The daily sum of (0.5 - close location) x next-day excess return has mean 0.0061 (t 3.26, 853 days) on the third of days whose range is widest against its 20-day average. On mid-width days it is 0.0022 (t 1.87, 1,007 days), and on narrow days 0.0003 (t 0.23, 811 days). Wide days carry about twice the measure's average of 0.0031 per day.
- **F3:** The effect also lives in agitated stretches. The same measure is 0.0068 (t 3.18, 652 days) when the coin's 20-day swing is above its 60-day average, against 0.0005 (t 0.28, 859 days) when it is below.
- **F4:** The effect fades within about a day. On a non-overlapping 2-day grid, the lowest-close quintile earns only +0.17 % (t 0.65), the second +0.79 % (t 2.75) and the fourth -0.60 % (t -2.36). On a 3-day grid no quintile reaches |t| 1.2.
- **F5:** A large one-day fall is followed by a rise the next day, and it is the strongest single pattern seen. The quintile of largest down days has a next-day excess of +0.71 % (t 4.56, 1,722 cases). The other quintiles run from -0.05 % to -0.31 % (t -0.36 to -2.59).
- **F6:** The 60-day trend does not separate the close-location effect clearly. The measure is 0.0061 (t 1.90) in falling markets, 0.0022 (t 1.61) in choppy ones and -0.0012 (t -0.51) in rising ones. None stands out given the number of angles looked at.
- **F7:** Weekday splits did not stand out after counting the angles looked at.
- **F8:** The tested book cannot pay at its present move size.

## Ideas
- `033-01.g1_wide-day-low-close-rebound` (from F1, F2, F4, F8): The wider a coin's day is against its usual daily range, and the nearer its close sits to that day's low, the larger its rise over the next day.
- `033-01.g2_agitated-close-near-low-rebound` (from F3, F1, F8): In an agitated market, the nearer a coin's daily close sits to that day's low, measured as its position within the day's high-low range, the larger the rise in its price over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `033-01.g3_sharp-daily-fall-rebounds` (from F5): The larger a coin's one-day fall, measured against its usual daily swing over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
