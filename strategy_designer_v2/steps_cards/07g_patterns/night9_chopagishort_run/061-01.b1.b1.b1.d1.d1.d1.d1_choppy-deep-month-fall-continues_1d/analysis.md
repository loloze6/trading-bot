---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4338 USD
---
## Findings
- **F1:** In choppy markets on folds B and C, the deeper the 20-day fall, the more the coin lags its 5-day drift. Falls of 10–15 % were followed by −3.3 % (15 cases, t −2.39), falls of 15–20 % by −8.6 % (16 cases, t −2.18) and falls of 20–30 % by −11.6 % (10 cases, t −1.62). Shallow falls of 0–10 % were followed by only −1.0 % to −3.0 % (t −0.33 and −1.94). This is the tested idea's grading, but on few cases.
- **F2:** Deep 20-day falls (−10 % or worse) kept falling in calm markets in all three trends. Falling calm: −3.5 % over 5 days (112 cases, 36 days, t −1.98). Choppy calm: −6.9 % (28 cases, t −1.99). Rising calm: −8.8 % (17 cases, t −1.96).
- **F3:** In falling agitated markets the same deep falls did not continue: +1.1 % (185 cases, 48 days, t +0.48). Falls deeper than 30 % in falling markets gave −0.05 % (88 cases, t −0.02). The continuation is a calm-market effect, and the agitated side is the rebound family the profile map already holds (16 falling-agitated long books).
- **F4:** One window carries the whole book. Summed over coin-days in a position, the book made +0.19, while w16 alone made +1.23. Without w16 it lost about −1.04, with w11 at −0.38, w17 at −0.47 and w18 at −0.24. This fits the failed one-window-left-out Sharpe of −0.147.
- **F5:** On days in a position the book's daily return moved against the coin's, as a short should (correlation −0.74 over 1,222 coin-days). The coins fell −0.39 % a day on those days, yet the book earned only +0.015 % a day. Most of the coins' fall did not reach the book after sizing and timing.
- **F6:** The brief's own pattern shows only weakly. In choppy agitated markets, closes in the top fifth of the day's range were followed by −4.6 % over 5 days, but on 10 cases over 9 days (t −2.51), after many angles were tried. In choppy calm markets the same closes were followed by +3.6 % (34 cases, t +0.90). These checks used each window's own median swing, not the profile's past-year median. This is too thin to count as a finding on its own.
- **F7:** Weekday and range width showed nothing that stands out after this many angles. No weekday reached |t| 1.8 (Wednesday −2.4 %, t −1.77). No range tercile within a trend reached |t| 1.9 (rising mid-range +2.5 %, t 1.87).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d1.d1.d1.g1_calm-deep-month-fall-continues` (from F2, F3, F1): In a calm market, a coin whose 20-day return is a deep fall keeps falling over the next five days, and the deeper that 20-day fall, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
