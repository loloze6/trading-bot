---
line: 7.g patterns
backtest: 086-02.c2_quiet-three-day-rise-continuation_1d
idea tested: 086-02.c2_quiet-three-day-rise-continuation
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3957 USD
---
## Findings
- **F1:** In falling calm markets, a coin's 5-day excess return grows with how far its close stands above its lowest close of the last 20 days (log distance): day-clustered t 2.75 on 121 grid cases over 83 days. Measured from the 10-day low, t is 3.04 on 129 cases over 87 days. At a 3-day horizon, t is 3.29 on 216 cases over 148 days.
- **F2:** The same measure outside falling calm carries nothing: t 0.05 at 5 days on 572 cases and t -0.16 at 3 days on 932 cases. The pattern lives in this profile only.
- **F3:** The effect is large and graded across the 20-day distance terciles at 5 days:
- **F4:** The effect points the same way on every coin, with Spearman 0.12 (BCH, 18 cases), 0.24 (ETH, 44), 0.28 (XMR, 27) and 0.37 (ZEC, 32). It also points the same way in 3 of 4 years, at 0.21 (2018), 0.17 (2019) and 0.37 (2021). The exception is 2020 at -0.004 on 15 cases.
- **F5:** Scaling the distance from the 20-day low by the coin's 20-day swing keeps the effect, at t 3.25 (3 days, 216 cases) and t 2.87 (5 days, 121 cases). The effect is gone by 10 days, at t 0.93 on 57 cases, so it is a short follow-through.
- **F6:** The tested situation is not supported. Falling-calm grid cases average a 5-day excess of -0.83 % (t -1.0, 146 cases). The up-day volume slope (t -2.05 at 5 days, 54 cases) flips sign across coins: Spearman +0.82 on BCH and -0.61 on ZEC. The volume of a rise is not a finding here.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `086-02.c2.g1_calm-decline-lift-off-low` (from F1, F2, F3, F4): In a falling, calm market, the further a coin's close has risen above its lowest close of the last 20 days, the larger its rise over the next 3 days.
- `086-02.c2.g2_swing-scaled-low-rebound` (from F3, F4, F5): In a falling, calm market, the larger a coin's rise above its lowest close of the last 20 days measured in units of its own 20-day swing, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
