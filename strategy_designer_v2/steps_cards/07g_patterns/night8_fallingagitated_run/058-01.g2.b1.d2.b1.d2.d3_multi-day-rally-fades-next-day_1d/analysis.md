---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6634 USD
---
## Findings
- **F1:** Inside the falling-agitated profile, an up day is followed by a fall the next day whatever its size. Over all up days the mean unusual move in the short direction is +0.96 % (t 2.48, 718 cases). But the up day's size against the 30-day swing does not grade it (Spearman rho 0.000, p 0.99, n 639; the largest quartile, at 1.43 swings, gives only -0.11 % next day, t -0.14).
- **F2:** Among in-profile up days that come after a fall over the four days before, the larger that prior fall against the 30-day swing, the larger the next-day fall (rho 0.233, p < 0.0001, n 380; three days ahead rho 0.215, p 0.012, n 135).
- **F3:** The bounce-fade of F2 holds in every year seen: the deeper-fall half gives +1.80 %, +1.19 %, +2.82 % and +2.24 % next day in 2018 to 2021. Over all prior-fall depths it is positive on 9 of 10 coins; DOGE is the exception, at -1.31 % with 10 cases.
- **F4:** Outside the profile the same bounce-fade is present but weaker (rho 0.076, p 0.0014, n 1,787). Its deepest-fall quartile gives +1.00 % next day (t 2.32) and +2.57 % over three days (t 2.30), so in profile it is about twice as large per case.
- **F5:** The brief's grading is not in these bars, and it runs the other way.
- **F6:** In profile, the one-day return reverts much more than outside it. The Spearman rho of the day's return in swings with the next-day unusual move is -0.208 in profile (n 1,297) against -0.080 outside (n 6,967).
- **F7:** In profile, wide-range days that close low or mid-range rebound next day by +2.43 % (131 cases) and +2.98 % (85 cases). That is the agitated wide-range low-close rebound already held (045-01, 039-02), not new. No weekday stood out: in-profile weekday means range from -0.70 % to +1.25 % on about 210 cases each.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.b1.d2.b1.d2.d3.g1_falling-agitated-bounce-fade` (from F2, F3, F4, F1): In a falling, agitated market, when a coin closes up after falling over the four days before, it gives part of that up day back over the next day. The deeper the four-day fall against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
