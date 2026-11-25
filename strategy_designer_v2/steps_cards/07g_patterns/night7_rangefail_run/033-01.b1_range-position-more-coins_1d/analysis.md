---
line: 7.g patterns
backtest: 033-01.b1_range-position-more-coins_1d
idea tested: 033-01.b1_range-position-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4165 USD
---
## Findings
- **F1:** The tested effect sits almost entirely in the upper part of the range. On the 5-day grid, closes at a new 20-day closing high are followed by a 5-day excess return of +5.77 % (t 2.29 with same-day cases taken together; 196 cases on 80 days). Closes at a new 20-day low are followed by -0.83 % (t -0.40; 228 cases on 65 days), not the mirror fall the idea claims.
- **F2:** The grading holds inside the upper half and not inside the lower half. Within the upper half, the slope of the 5-day excess return on range position is +3.36 % per unit (t 1.30; 966 cases, 181 days), with quintiles 4 and 5 at +1.30 % (t 2.16) and +2.97 % (t 2.54). Within the lower half the slope has the wrong sign, -1.21 % (t -0.51; 1050 cases, 197 days), and the lowest quintile sits at -0.13 % (t -0.11).
- **F3:** The book earns on the long side and loses on the short side. Long trades average +8.60 % net (median -0.84 %, 2919 trades), while short trades average -1.13 % net (median -2.65 %, 3339 trades). The book's daily returns correlate -0.17 with its coins' daily returns over 1449 days.
- **F4:** How much a close beyond the prior range pays is not graded by its distance from that range. Measured in units of 20-day volatility, the slope above the prior 20-day high is +4.58 % (t 1.02; 193 cases, 78 days). Below the prior 20-day low it is -1.77 % (t -0.88; 211 cases, 61 days).
- **F5:** The range-position slope is positive in rising and choppy markets and weaker in falling ones. It is +3.92 % per unit in rising markets (t 2.26; 484 cases, 84 days) and +9.91 % in choppy markets (t 2.04; 189 cases, 76 days). In falling markets it is +2.12 % (t 1.29; 527 cases, 100 days), and in falling agitated markets +0.11 % (t 0.04).
- **F6:** Several angles showed nothing that stands out once same-day cases are taken together:

## Ideas
- `033-01.b1.g1_upper-range-strength-keeps-rising` (from F1, F2, F3): The higher a coin's daily close sits in the upper half of its own 20-day closing range, the more the coin rises over the next 5 days. The rise is largest when the close is at the top of that range.
- `033-01.b1.g2_range-position-in-rising-markets` (from F5, F1): In a rising market, the higher a coin's daily close sits within its own 20-day high-to-low range, the more the coin rises over the next 5 days. A close at the top of the range is followed by the largest rise, and a close at the bottom by the largest fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
