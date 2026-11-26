---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d
idea tested: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5993 USD
---
## Findings
- **F1:** In the falling-agitated profile, the next-day move after a down day grows with the fall times the close's depth below its 20-day high. By quartile of that product it goes +0.18 % (167 cases, 98 days, t 0.23), +0.61 % (t 0.95), +1.03 % (t 2.20) and +3.17 % (167 cases, 72 days, t 2.56). By fall size alone it runs +0.55 %, +1.11 %, +2.17 % and +6.20 % from the smallest falls to falls of more than 2 usual moves, with every t by days under 2 (1.44 to 1.93). This rebound is the long side the profile map already holds 12 times in falling agitated (scaled-fall, drop-vs-range and daily-fall rebounds), so it is no discovery.
- **F2:** In the profile, a 3-day rise measured in usual 3-day swings is given back over the next 3 days in step with its size. By tercile on the 3-day grid the unusual move is +0.56 % (61 cases, 38 days, t 0.34), -0.58 % (t -0.40) and -2.94 % (58 cases, 29 days, t -1.66). Outside the profile, 3-day rises of 0.5 to 1.5 swings continue by +1.01 % (465 cases, 190 days, t 1.90) and those above 1.5 swings by +1.82 % (t 1.41), so the give-back after several days is the profile's own. It is suggestive, not sure.
- **F3:** The tested one-day fade does not grow past one usual move. Inside the profile, rises of 0 to 0.5 usual moves are followed by -0.95 % (354 bars, t -3.31) and rises of 0.5 to 1 by -1.17 % (t -2.13). Rises of 1 to 2 are followed by only -0.17 % (t -0.32) and rises above 2 by +0.21 %.
- **F4:** The depth term of the tested forecast does not grade the fade. On up days inside the profile, the shallowest depth quartile (close within 9 % of the 20-day high) fades -0.82 % (216 bars, t -2.88), while the deepest quartile fades -0.90 % (139 bars, t -1.41). Up days in the top half of their range fade -1.07 % and -0.76 % (t -3.02 and -2.37), and those closing in the lower quarter fade +0.10 % (14 bars).
- **F5:** The book's short positions inside the profile earned +0.19 % per position-bar before costs (666 bars), which is less than the 0.22 % one trade costs.
- **F6:** None of the other angles stood out from the ~60 cells looked at:

## Ideas
- `058-01.g2.b1.d2.b1.d2.g1_multi-day-rally-give-back` (from F2, F3): In a falling, agitated market, the larger a coin's rise over the past 3 days against its usual 3-day swing (the standard deviation of its daily returns over the past 30 days, scaled to 3 days), the larger the fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
