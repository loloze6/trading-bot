---
line: 7.g patterns
backtest: 043-01_falling-market-narrow-day-rise_1d
idea tested: 043-01_falling-market-narrow-day-rise
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3624 USD
---
## Findings
- **F1:** Inside the falling profile, the narrowest fifth of days (range against the 30-day swing) is followed by a 3-day move +2.29 % above the coin's normal drift (196 cases on 96 days, day-clustered t 2.13), while the other four fifths are flat to negative (−0.49 %, +0.42 %, −1.19 % with t −2.39, −0.89 %). The regression slope has t −2.26 on 1,130 cases. The effect sits in the narrowest days and does not grow steadily across the range. All six coins are positive in that fifth (+1.5 % to +3.4 %).
- **F2:** The narrow-day rise in falling markets is concentrated in the deeper declines. Where the 60-day return is below the coin's falling-profile median, the narrowest fifth is followed by +5.56 % excess over 3 days, against +0.88 % where the decline is shallower. The other fifths are −0.4 % to −2.1 % in both halves.
- **F3:** By year, the narrow-day rise in falling markets is uneven: +3.23 % in 2018 (76 cases), −0.16 % in 2019 (45), +4.06 % in 2020 (49) and +0.42 % in 2021 (26). By window it ranges from −2.1 % to +17 %, and w9 (−0.22 %, 32 cases) and w18 (−1.63 %, 20 cases) are negative.
- **F4:** The book lost because of its shorts on wide falling-profile days. They summed −0.85 against −0.10 for its longs, with a mean daily gain of −0.046 % on 1,846 short bars against −0.003 % on 3,093 long bars. Its Sharpe was −0.59 over a 0.19 % cost per trade, so the long-only narrow-day part carried no loss of its own.
- **F5:** Outside the falling profile, the widest fifth of days is followed by +2.01 % excess over 3 days (278 cases on 132 days, day-clustered t 2.21). The whole gain comes from wide days that closed down: +4.27 % on 126 cases, against +0.14 % on 152 wide up days.
- **F6:** The wide-day rebound outside falling markets is strongest in rising markets: +3.42 % in the widest fifth when the 60-day return is above +10 %, against +0.55 % otherwise. It is positive on all six coins (+0.9 % to +4.7 %) and in all four years (+0.4 % to +3.0 %). Inside the falling profile, wide days are followed by −0.89 %.
- **F7:** Next-day returns after Thursday and Friday closes are +0.61 % (t 4.10) and +0.52 % (t 3.87), positive on every coin and in every year. Clustered by day the t is only 2.14 over 413 days, and a weekday effect cannot be graded, so it is noted but not proposed.

## Ideas
- `043-01.g1_quiet-day-after-deep-slide` (from F1, F2, F3): In a falling market, a day whose high-low range is narrow against the coin's 30-day daily-return swing is followed by a rise over the next 3 days, and the rise is larger the deeper the coin's decline over the last 60 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `043-01.g2_uptrend-wide-down-day-rebound` (from F5, F6): In a rising market, a day that closes down with a high-low range wide against the coin's 30-day daily-return swing is followed by a rise over the next 3 days, and the rise is larger the wider the day's range against that swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
