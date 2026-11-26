---
line: 7.g patterns
backtest: 047-01_falling-agitated-scaled-fall-rebound_1d
idea tested: 047-01_falling-agitated-scaled-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6015 USD
---
## Findings
- **F1:** Outside the tested profile, in coins not in a rising trend, the 5-day return scaled by the 30-day daily swing carries on over the following days. The slope of the unusual move on it is +0.0179 over 3 days (t 2.46, 591 cases on 186 days) and +0.0344 over 5 days (t 3.04, 344 cases on 110 days), with day-clustered t's.
- **F2:** Bucketed on 3-day grid cases outside the profile, the 3-day unusual move rises steadily with the scaled 5-day move. It is −2.46 % (t −2.96, 171 cases) after a 5-day fall of 1 to 2 usual moves, and +1.30 % (t 2.31, 247 cases) after a 5-day rise of 1 to 2 usual moves. Pooled over all trends outside the profile, the slope is +0.0091 (t 2.15, 1,899 cases on 391 days).
- **F3:** The carry-on is weaker when the coin is rising: the slope is +0.0042 over 3 days (t 0.49) and +0.0196 over 5 days (t 1.76).
- **F4:** Inside the falling-agitated profile, the 5-day scaled move has a negative slope (−0.0071, t −0.57), the opposite sign to outside it.
- **F5:** The tested down-day side is not graded in a way that can be told from chance. Inside the profile:
- **F6:** The book's worst 2 % of days average −2.72 %, against −9.02 % for the coins on those days. That is about a third of the coins' fall on those days, consistent with being in the market on 21 % of coin-days.
- **F7:** The Wednesday bar's next-day unusual return (−0.50 %, t −2.78 on bars) loses its strength once same-day cases are taken together (t −1.26). It is not a finding to act on.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `047-01.g1_scaled-five-day-move-continues` (from F1, F2, F3): When a coin has moved far over 5 days against its usual daily swing of the past 30 days, it keeps moving the same way over the next 5 days, and the larger that 5-day move in units of the swing, the larger the move that follows.
- `047-01.g2_calm-downtrend-move-continues` (from F1, F3, F4): In a falling, calm market, the larger a coin's 5-day return in units of its 30-day daily swing, the further the coin moves the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
