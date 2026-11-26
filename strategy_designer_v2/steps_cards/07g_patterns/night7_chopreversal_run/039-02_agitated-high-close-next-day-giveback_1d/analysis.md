---
line: 7.g patterns
backtest: 039-02_agitated-high-close-next-day-giveback_1d
idea tested: 039-02_agitated-high-close-next-day-giveback
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4253 USD
---
## Findings
- **F1:** In agitated markets the close-location effect sits entirely in falling and choppy trends: the slope of the standardised next-day return on close location is -0.78 (t -2.66, 738 bars) when the 60-day trend is below -10 % and -1.27 (t -2.13, 120 bars) when it is between -10 % and +10 %, but +0.12 (t 0.60, 755 bars) in a rising trend.
- **F2:** In agitated markets, close location adds nothing once the day's own return scaled by its 20-day swing is known: alone its slope is -0.34 (t -2.97, 3333 bars), and next to that scaled return it drops to -0.15 (t -0.69). In a falling agitated market the scaled day return keeps its slope next to close location (-0.31, t -2.08), while close location falls to -0.02 (t -0.04).
- **F3:** The reversal comes from down days only. In agitated markets the scaled-return slope is -0.25 on down days (t -2.14, 1636 bars) and +0.08 on up days (t 1.41, 1696 bars), and the close-location slope is -0.35 on down days (t -1.48) and +0.03 on up days (t 0.14). After a fall of 2 or more usual swings, the next day is +0.86 standard deviations in agitated markets (75 cases) against -0.01 in calm ones (122 cases). After falls of 1.5 swings or more it is positive in every year (+0.24 to +0.59) and on every coin (+0.27 to +0.54).
- **F4:** In agitated markets close location is graded by the day's width: its slope is -0.68 (t -3.40, 1128 bars) on days whose range is in the widest third against the coin's 30-day mean range, against -0.18 (t -1.15) in the narrowest third. Location times relative width has a slope of -0.29 (t -3.46, 7709 bars, all profiles).
- **F5:** The effect lasts one day only. The agitated close-location slope is -0.15 (t -1.00, 1840 cases) over 2 days and -0.10 (t -0.60, 1219 cases) over 3 days, on non-overlapping grids.
- **F6:** The book's gain is thin against its swings. Its mean is +0.015 % a day over 1449 days, for a sum of +0.22. Its best 5 % of days sum to +0.55 and its worst 5 % to -0.51. That fits a 0.39 % unusual move per case that covers a 0.19 % trade only twice and is spread over every agitated day, including the rising ones where F1 shows no effect.
- **F7:** The weekday pattern does not stand out after this many angles. Signals on Wednesday score -0.09 (t -2.82) and on Thursday +0.08 (t 2.84), but neither holds by year (Thursday 2021 -0.003, Wednesday 2021 +0.03).

## Ideas
- `039-02.g2_downtrend-low-close-next-day-rebound` (from F1, F6): In a falling, agitated market, the lower a coin closes within its day's high-low range, the larger its rise over the next day.
- `039-02.g3_wide-day-close-location-reversal` (from F4, F6): In an agitated market, the lower a coin closes within a day whose high-low range is wide compared with its last 30 days' ranges, the larger its rise over the next day, and the wider the day, the larger the rise.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `039-02.g1_agitated-downtrend-capitulation-rebound` (from F2, F3, F1): In a falling, agitated market, the larger a coin's one-day fall measured against its usual daily swing, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
