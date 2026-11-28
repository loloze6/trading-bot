---
line: 7.c no effect
backtest: 086-02_repeated-heavy-volume-buying-days_1d
idea tested: 086-02_repeated-heavy-volume-buying-days
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4037 USD
---
## Findings
- **F1:** In falling calm markets, single up days on the heaviest third of volume against the 20-day average were followed by 5-day returns 2.79 % below the coin's normal drift (21 cases, 17 days, t -1.26), and up days on the lightest third were followed by 4.44 % above it (16 cases, 14 days, t +1.71): the brief's heavy-against-light comparison points the other way.
- **F2:** Inside falling calm, the up-day volume ratio is ranked against the later excess return with a Spearman rho of -0.19 over 5 days (54 up days) and -0.185 over 3 days (109 up days): the heavier the volume, the smaller the follow-through, the opposite of the brief's grading.
- **F3:** Outside falling calm, heavy-volume up days were followed by excess returns of +3.29 % over 5 days (82 cases, 56 days, t 1.84) and +5.36 % over 10 days (37 cases, t 1.83), while light-volume up days gave -0.42 % over 5 days (91 cases, t -0.36): the brief's effect appears only in other profiles, off this run's box.
- **F4:** Inside falling calm, 3-day rises in the lowest quartile of 3-day volume against the prior 20 days were followed by +4.57 % excess over 5 days (14 cases, 13 days, t 1.66). The higher three volume quartiles gave about 0 % (-0.04 %, -0.01 %, -0.40 %; 40 cases).
- **F5:** Inside falling calm, 3-day falls on the lightest 3-day volume were followed by -4.26 % excess over 5 days (16 cases, t -3.06) and -3.67 % over 3 days (31 cases, t -3.61): quiet declines keep declining.
- **F6:** Inside falling calm, the two lowest quintiles of the 3-day return were followed by 5-day excess returns of -4.54 % (t -1.76) and -3.09 % (t -2.03), against +3.28 % for the fourth quintile (t 1.73), from 23 to 24 cases each. The tested forecast's 285 cases gave an unusual move of -0.03 % (t -0.05), so the size it captured is nil against a 0.31 % trade cost.
- **F7:** The pattern is uneven across coins (5-day excess after heavy up days: XMR +2.93 % from 7 cases, ZEC -2.90 % from 7, ETH -8.75 % from 3). Light up days were positive in 2018 (+4.54 %), 2021 (+7.33 %, t 2.02) and in ETH, XMR and ZEC. Every cell holds fewer than 10 cases.

## Ideas
- `086-02.c1_light-volume-up-day-follow-through` (from F1, F2, F7): In a falling, calm market, an up day on volume light against the coin's 20-day average volume is followed by a rise over the next 5 days, and the lighter that day's volume, the larger the rise.
- `086-02.c2_quiet-three-day-rise-continuation` (from F4, F2, F6): In a falling, calm market, the lighter a coin's volume over a 3-day rise against its prior 20-day average volume, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
