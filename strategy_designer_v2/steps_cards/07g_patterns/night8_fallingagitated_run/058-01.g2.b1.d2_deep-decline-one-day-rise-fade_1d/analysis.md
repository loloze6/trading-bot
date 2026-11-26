---
line: 7.g patterns
backtest: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade_1d
idea tested: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5648 USD
---
## Findings
- **F1:** In falling markets that are not agitated (60-day return below -10 %, outside the tested profile), the move over the next days follows the coin's recent move scaled by its 30-day swing. The 5-day return in swing units has a slope of +1.84 % per unit on the next 3-day unusual move (day-clustered t 2.42, 458 cases on 141 days). The 3-day return has a slope of +2.64 % per unit on the next 5-day move (t 2.49, 265 cases on 81 days). The extreme fifths also point this way: the lowest 5-day-return fifth averages -2.93 % over 3 days (t -1.69) and the highest +2.16 % (t 1.85). Both are about ten times the 0.22 % cost of a trade.
- **F2:** This continuation in falling calm markets is not even across windows. The correlation of the 3-day rise with the next 3-day move is positive in 5 of 8 windows (+0.33 and +0.34 in the two largest after w7 and w9), and negative in w7 (-0.12, 84 cases), w9 (-0.10, 79) and w16 (-0.53, 10). It is the strongest pattern found, but it only just stands out given how many angles were checked.
- **F3:** Inside the tested profile (falling agitated), the brief's own direction, a few-day rise given back, shows but cannot be told from chance:
- **F4:** The tested one-day-rise fade does not hold up as graded. In the profile, the 3-day move by fifth of one-day rise runs +3.55 %, -0.89 %, +1.85 %, -0.78 %, -2.39 %, which is not monotone. The step-5 size was +0.56 % (t 1.34), and the correlation of |forecast| with the move was only 0.02.
- **F5:** Outside falling markets no comparable graded pattern stands out:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.b1.d2.g1_falling-calm-swing-momentum` (from F1, F2, F5): In a falling, calm market, the larger a coin's 5-day return against the standard deviation of its daily returns over the past 30 days, the further its price moves the same way over the next 3 to 5 days: larger falls are followed by larger further falls, larger rises by larger further rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
