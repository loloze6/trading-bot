# The planted-effect test of step 5

**Question.** Every verdict so far is inconclusive. Is step 5 able to say "confirmed" or "rejected" at all, or is something broken?

**What was done.** Two real fold-A records (002-05, a steady relation; 001-01, an extreme, on BTC and ETH) were copied, and a known drift was added to each next-bar return in the direction of the forecast: r' = r + delta x sign(forecast). Prices were rebuilt from those returns; the forecast and indicator columns were left unchanged. Step 5 ran unchanged, closed book, on each copy (`make_planted.py`, `records/`, `plans/`, `verdicts/`). These records are not market evidence. Cost: 0.68 USD.

| Plan | Planted drift per day | Status | Main statistic |
|---|---|---|---|
| 002-05 | none | inconclusive | Welch t 0.70 |
| 002-05 | +0.1 % | inconclusive | 1.18 |
| 002-05 | +1 % | **confirmed** | 5.54 |
| 002-05 | -1 % | **rejected** | -4.14 |
| 001-01 | none | inconclusive | t -1.32 |
| 001-01 | +0.1 % | inconclusive | -1.52 |
| 001-01 | +1 % | **confirmed** | -3.33 (the idea's direction is a fall) |
| 001-01 | -1 % | inconclusive | +0.59 |

**Step 5 is not broken.** It confirms and rejects planted effects, in the right direction. Every situation check passed.

**But its reach is short on this data.**
- In 002-05, +1 %/day moves t by 4.8: the standard error of the in-trend minus out-of-trend daily return is about 0.21 %. To reach t = 2, the true difference must be about 0.4 % a day, roughly +150 % a year. A strong realistic edge (+0.1 %/day) moves t by 0.5 only.
- In 001-01, the drift moves the 5-bar measure by about ±1.7 %, symmetrically; -1 % stays inconclusive only because the real data starts at -1.2 %. Half of the planted drift is lost because the plan's baseline (holding: the mean over all bars) includes the active bars themselves, which are half the bars.

**Why hourly bars did not help.** For an edge of steady size, the t-statistic is about the annual Sharpe ratio times the square root of the years covered; the number of bars does not enter. Fold A is 2 years: t = 2 needs an annual Sharpe of about 1.4 before costs. With 8 years it needs about 0.7.

**Conclusion.** Not a bug, and the threshold (t of 2) is the usual one. The sample is too small: 2 years and 1 or 2 coins. The next run widens it (`../../FULL_DATA_RUN.md`).
