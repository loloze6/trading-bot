---
line: 7.g patterns
backtest: 036-01_agitated-scaled-fall-three-day-rebound_1d
idea tested: 036-01_agitated-scaled-fall-three-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3935 USD
---
## Findings
- **F1:** In the agitated bars of folds B–C, the slope of the 3-day excess return on the scaled one-day return (z = day's return / 30-day std of daily returns) is −2.84 % per unit of z in a falling 60-day trend (t −2.41, day-clustered; 242 cases on 75 days), against +0.65 % in a rising trend (t 0.44; 242 cases, 87 days) and +0.30 % in a choppy trend (t 0.14; 40 cases), so the graded rebound after a scaled fall shows only where the coin has fallen more than 10 % over 60 days.
- **F2:** Over all agitated bars together the same slope is only −0.75 % per unit of z (t −1.12; 963 cases, 298 days), although the two lowest z septiles (z below −0.39) are followed by +1.75 % and +1.97 % excess 3-day returns (t 1.65 and 2.01, 118 and 134 cases); outside a falling trend the tested idea is too weak to tell from zero.
- **F3:** In calm bars, the 3-day excess return grows with the coin's 5-day return scaled by its usual swing (slope +0.94 % per unit, day-clustered t 2.36; 1,298 cases, 327 days) and with its 20-day scaled return (+0.76 %, t 2.13); in agitated bars the same slopes are +0.28 % (t 0.37) and +0.17 % (t 0.28); every coin's 20-day slope is positive (t 0.78 to 1.80), but only 6 of 12 windows are.
- **F4:** Pooled over all regimes, the 3-day excess return is −1.45 % after the lowest quintile of the 20-day scaled return (t −3.41, 453 cases) and +1.27 % after the fourth quintile (t 3.25), with +0.58 % in the top quintile (t 1.31); these t's are not day-clustered, so they overstate how sure the pattern is.
- **F5:** The next-day excess return differs by weekday: Thursday +0.41 % (t 2.80), Friday +0.38 % (t 2.74), Wednesday −0.50 % (t −2.78). The Thursday+Friday minus Monday+Wednesday gap is large in 2019 (t 7.48) and 2020 (t 2.20) but small in 2018 (t 1.23) and 2021 (t 0.54). It is an ungraded calendar effect, and its t counts coins on the same day separately, so it gives no idea.
- **F6:** The book behaves like market exposure, not timing. Its worst 5 % of days average −3.50 % while the coins average −8.75 % on those days, and its best 5 % average +3.35 % against the coins' +7.82 %. Its mean trade return does not rise with the entry forecast: by forecast quartile, +3.04 %, +0.96 %, −0.38 % and +2.02 %.
- **F7:** The 3-day excess return is not graded by the day's range against the usual swing: by quintile it is +1.00 %, −1.12 %, −0.15 %, −0.35 % and +0.88 %, a U shape with no direction. It does not change with where the day closes in its range either: by quintile it runs from −0.10 % to +0.15 %, every |t| below 0.4.

## Ideas
- `036-01.g1_falling-agitated-scaled-fall-rebound` (from F1, F2): In a falling, agitated market, the larger a coin's one-day fall against its 30-day daily swing, the larger its rise over the next three days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `036-01.g2_calm-market-short-term-momentum` (from F3, F4): In a calm market, the larger a coin's 5-day return against its 30-day daily swing, the larger its move the same way over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
