---
line: 7.c no effect
backtest: 086-02.c1_light-volume-up-day-follow-through_1d
idea tested: 086-02.c1_light-volume-up-day-follow-through
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4053 USD
---
## Findings
- **F1:** In falling calm markets the tested light-volume up days show almost no follow-through: the verdict's unusual 5-day move is +0.18 % (t 0.41, 408 days, strength 0.017). In my recomputation, up days in the lightest volume quartile (volume under 0.52 of the prior 20-day mean) gained +1.78 % unusual over 5 days (t 1.41, 52 cases), and the middle quartiles lost −0.69 % and −0.72 %.
- **F2:** Over 5 days the brief's own heavy-volume up days were given back: the heaviest quartile (above 1.22 of the 20-day mean) lost −1.54 % unusual (t −1.28, 54 cases). Volume against later move on up days has a Spearman of −0.10 (p 0.23, 137 cases). So the market leaned against the brief's heavy-volume reading, but weakly.
- **F3:** The light-volume follow-through holds only when the coin's last 10 days fell less than the median. There, the lightest-quartile up days gained +2.75 % unusual over 3 days (t 2.39, 27 days), +5.16 % over 5 days (t 3.15, 21 days) and +7.75 % over 10 days (t 2.23, 15 days). After a deeper 10-day fall they gained about 0 (−0.05 % over 5 days, t −0.03, 31 days).
- **F4:** After a deeper 10-day fall, the other up days (not in the lightest quartile) kept falling. They lost −1.83 % unusual over 3 days (t −2.25, 72 days) and −3.15 % over 5 days (t −2.20, 54 days). After a shallower fall the same days gained +1.39 % over 5 days (t 1.12, 49 days).
- **F5:** Across all falling-calm days, the later move grows with how shallow the 10-day fall was. By tercile of the 10-day return, the 5-day unusual move is −2.13 % (deep fall, t −1.65), −1.34 % (mid, t −1.30) and +0.47 % (shallow, t 0.43). Over 10 days it is −4.60 % (t −2.29), −3.32 % (t −1.49) and +2.06 % (t 1.02).
- **F6:** The result depends on the year, whatever the volume. Falling-calm up days lost money over 5 days in 2018 and 2019: heaviest quartile −7.99 % (t −2.70) in 2018, middle quartiles about −5 % (t −3.1 and −3.0) in 2019. In 2020 and 2021 they gained in most quartiles: lightest quartile +5.77 % (t 2.75) in 2021.
- **F7:** By coin, the lightest-quartile up days gained over 5 days on ETH (+3.87 %, 11 cases), ZEC (+2.03 %, 22 cases) and BCH (+1.49 %, 7 cases), and about 0 on XMR (−0.41 %, 12 cases). On ETH the other up days lost −3.85 % (t −2.10, 41 cases).
- **F8:** The size is too small to pay. The unusual move of +0.18 % per case is 0.6 times the 0.31 % cost of a trade, so only an idea with a larger move per case, like the shallow-fall cases of F3 (+5.16 % over 5 days), could cover cost beyond drift.

## Ideas
- `086-02.c1.c1_light-up-day-shallow-fall` (from F1, F3, F7, F8): In a falling, calm market, an up day on volume light against the coin's 20-day average is followed by a rise over the next 5 days, only while the coin's 10-day fall before that day is shallow; the lighter the volume and the smaller that 10-day fall, the larger the rise.
- `086-02.c1.c2_up-day-after-shallow-fall` (from F4, F5, F2): In a falling, calm market, an up day is followed by a rise over the next 5 days that is larger the less the coin fell over the 10 days before it, and it is given back after a steep 10-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
