---
line: 7.g patterns
backtest: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade_1d
idea tested: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4415 USD
---
## Findings
- **F1:** Across every trend, fading where a day closes in its range only pays when the coin is swinging more than its own usual. On the half of days with the largest |close-off-middle × width|, the next-day drift-adjusted return in the fade's direction is +1.65 % long (602 cases, 254 days, t 2.99) and +1.11 % short (729 cases, 310 days, t 2.35) in each coin's highest tercile of 30-day swing. In the middle tercile it is +0.20 % long (t 0.67) and +0.44 % short (t 1.86). In the lowest tercile it is +0.09 % long (t 0.24) and −0.05 % short (t −0.20).
- **F2:** The fade's strength grows step by step with the coin's swing level. On the large-signal days it is −0.026, +0.070 and +0.173 of a usual move from low to high swing tercile. Over all days, the fade signed by direction is +0.02 % (t 0.28), +0.15 % (t 2.01) and +0.48 % (t 3.99) on 2,894, 2,886 and 2,894 cases.
- **F3:** Inside the high-swing tercile the effect is graded by the size of the signal on both sides. In the top quartile of |fade| it is +2.30 % long (344 cases, t 2.92) and +1.64 % short (380 cases, t 2.77). The bottom quartile gives +0.02 % long (t 0.05) and +0.50 % short (t 1.06).
- **F4:** The high-swing fade is stable across years and coins. It is positive in every year: 2018 +1.41 % (t 2.27), 2019 +0.89 % (t 1.63), 2020 +1.98 % (t 2.00), 2021 +1.24 % (t 2.14). It is also positive on all 10 coins, from BTC +0.58 % (t 1.67) to ADA +2.61 % (t 3.45) and XMR +1.63 % (t 3.49).
- **F5:** The tested profile catches only a small part of this effect. Choppy-agitated bars are 377 of about 8,700 bar-cases, and the book is in a position on 8 % of the coins' days. Its top fade quintile in profile gives +2.56 % (72 cases, t 2.58). Outside the profile the top quintile still gives +0.57 % (1,663 cases, t 1.96).
- **F6:** On the short side in the high-swing tercile, the fade fails in rising markets and holds in the others:
- **F7:** The reversal is over within one day. The second day after the signal, in the fade's direction, is −0.30 %, −0.14 % and −0.48 % by swing tercile (t −1.72, −0.77, −1.43): no further gain, and a slight give-back that cannot be told from zero.
- **F8:** No weekday pattern stands out in next-day drift-adjusted returns: all seven weekdays have |t| ≤ 1.0 (181 to 183 days each).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `077-03.g1.b1.d1.g1_agitation-scaled-wide-close-fade` (from F1, F2, F3, F4, F5, F7): In an agitated market, a wide day closing near its low rises over the next day and a wide day closing near its high falls over the next day. The move is larger the further the close sits from the middle of the range, the wider the day against the coin's 30-day swing of daily returns, and the more that 30-day swing exceeds its usual level over the past year.
- `077-03.g1.b1.d1.g2_falling-agitated-high-close-fade` (from F1, F3, F6): In a falling, agitated market, a wide day closing near its high falls over the next day, more so the wider the day against the coin's 30-day swing of daily returns and the closer its close to the day's high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
