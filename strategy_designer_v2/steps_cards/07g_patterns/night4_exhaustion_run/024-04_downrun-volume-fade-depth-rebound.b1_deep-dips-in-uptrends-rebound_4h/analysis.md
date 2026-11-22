---
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3922 USD
---
## Findings
- **F1:** The rebound is concentrated in the deepest down streaks. With the coin's 30-day return positive, streaks of more than 5 usual moves are followed by +6.45 % unusual 18-bar moves (t 4.23, 47 cases) and streaks of 3–5 usual moves by +2.21 % (t 2.13, 89 cases), while streaks of 0–3 usual moves give between −0.20 % and +0.23 % (all |t| < 0.3). With the 30-day return not positive, the deepest streaks still give +1.84 % (t 1.78, 72 cases).
- **F2:** Volume works against the brief. Deep down streaks (at least 2 usual moves) are followed by +2.17 % (t 3.72, 240 cases) when the last 8 hours' volume is in the top tercile against its 5-day mean, but only +0.30 % (t 0.47, 240 cases) when volume is fading. Deep up streaks show the same split: +2.26 % (t 2.92, 259 cases) with heavy volume against −0.31 % (t −0.59, 258 cases) with fading volume. So the coin rises after large runs in either direction when volume is heavy, and does not give back after fading volume.
- **F3:** The 1-day return, in usual moves, has a U-shape against the next 3 days. Its lowest decile is followed by +1.26 % unusual (t 3.58, 515 cases) and its highest by +1.07 % (t 2.43, 515 cases). Deciles 2 to 8 are all negative, from −0.24 % to −0.69 %.
- **F4:** The book's gain is carried by a few long trades. The longest-duration quartile of trades averages +27.85 % net, against +0.77 % to −2.88 % for the other three quartiles. The top entry-forecast quartile averages +14.25 % but its median is only +0.03 %.
- **F5:** Sunday grid cells are followed by −1.23 % unusual 18-bar moves (t −3.92, 811 cases), the only weekday below −0.4 %. Most cells start at hour 0, and about 100 groupings were examined, so this is noted but not graded into an idea.
- **F6:** In coins falling over 30 days, shallow down streaks (0–1 usual move) are followed by −1.07 % unusual moves (t −3.04, 505 cases). Given the number of cells examined, this is borderline.

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound.g1_heavy-volume-runs-precede-rises` (from F2, F1): After a 4-hour run that is large relative to the coin's typical 4-hour move over the past 30 days, in either direction, the coin rises over the next three days. The rise is larger the more the volume of the last 8 hours exceeds its 5-day average.
- `024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound.g2_extreme-days-precede-rises` (from F3, F1): The larger the coin's 1-day move in either direction, measured in its typical moves over the past 30 days, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
