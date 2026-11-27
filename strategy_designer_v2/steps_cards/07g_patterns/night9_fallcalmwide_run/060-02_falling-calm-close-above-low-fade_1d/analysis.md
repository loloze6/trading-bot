---
line: 7.g patterns
backtest: 060-02_falling-calm-close-above-low-fade_1d
idea tested: 060-02_falling-calm-close-above-low-fade
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5731 USD
---
## Findings
- **F1:** In a choppy agitated market, the day's close location times its range in usual moves ((close−low)/(high−low) − 0.5) × (high−low)/close / 30-day swing runs against the next day's excess return: r −0.33, t −4.70 over 182 days (238 coin-days, mostly XRP, ZEC, XMR, BTC). This is the strongest of all the angles looked at.
- **F2:** The F1 effect in choppy agitated keeps its sign in every year: r −0.48 in 2018 (t −2.52, 23 days), −0.31 in 2019 (t −2.89, 78 days), −0.39 in 2020 (t −2.58, 40 days) and −0.15 in 2021 (t −0.98, 41 days).
- **F3:** The F1 effect works on both halves of the day's range, more strongly on the low side. Among days closing in the lower half, r is −0.46 (t −5.02, 95 days); among days closing in the upper half, r is −0.20 (t −2.03, 99 days). All three terciles of the upper-half score are followed by a fall: −1.79 %, −2.34 % and −2.39 % next-day excess, at t −0.97 to −1.70.
- **F4:** The F1 effect sits in the next day. On a 2-day non-overlapping grid the correlation falls to r −0.18 (t −1.73, 95 days) in choppy agitated, and to r −0.14 (t −1.50, 114 days) in falling agitated.
- **F5:** The brief's effect is not in falling calm bars. Days in the top fifth of close location gave +0.02 % next-day excess (t 0.06, 113 days). Wide days that close high gave −0.51 % (t −1.04, 57 days). The score's correlation with the next day is r −0.07 (t −1.46, 405 days), and it is 0.00 % (t 0.00) over two days.
- **F6:** The same reversal exists in falling agitated, but most of it comes from one year. Overall r is −0.24 (t −3.88, 241 days), yet 2020 alone gives r −0.60 (t −4.24, 34 days), while the other years are between −0.12 and −0.18 with t under 1.6. This profile is already held: 058-02.b1.g1.b1.b1 and 060-01.g1.d2.d1 hold falling agitated shorts, and 16 books hold its longs.
- **F7:** Over all bars, the low-close rebound is the most reliable single cell. Wide days (top fifth of range) closing in the bottom fifth of their range gave +1.46 % next-day excess (t 3.02, 177 days), against −0.59 % (t −1.27) for wide days closing in the top fifth. The long side of this pattern is already held in the agitated profiles.
- **F8:** The book traded against its own idea half the time and lost. 47 % of its positions were long, only 51 % of its active bars were in the plan's situation, and it gained only on its widest-range days: +0.128 % per position-bar (t 2.24) in the top range fifth, against −0.043 % (t −2.28) in the bottom fifth. Its Sharpe was −0.31.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.g1_choppy-agitated-wide-close-reversal` (from F1, F2, F3, F4, F7): In a choppy, agitated market, a day's close location within its range, scaled by how wide that range is against the coin's 30-day swing of daily returns, is followed by a move the other way over the next day. The move is a rise after wide days closing near their low and a fall after wide days closing near their high, and it is larger the wider the day and the further the close sits from the middle of its range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
