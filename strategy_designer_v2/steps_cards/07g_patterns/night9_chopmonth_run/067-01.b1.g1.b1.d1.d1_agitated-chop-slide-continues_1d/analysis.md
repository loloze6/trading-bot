---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4434 USD
---
## Findings
- **F1:** The tested slide-continuation is weak in the bars of folds B and C. In choppy markets, the drift-adjusted 10-day move signed by the 30-day direction averages +2.4 % after falls, with a day-clustered t of 1.17 on average across the ten grid offsets (range 0.41 to 2.23, about 152 cases each). After rises it averages +1.5 % with a mean t of 0.59. So the effect does not show after rises, and after falls it cannot be told from chance on most grids.
- **F2:** The continuation that does show comes only from the deepest falls, and they bunch on a few days. In choppy markets, the lowest third of 30-day moves is followed by an unusual 10-day move of -16.5 % when agitated (15 cases on only 7 days, t -4.01) and -11.4 % when calm (11 cases on 8 days, t -2.23). The middle and upper thirds lie between -0.6 % and +5.5 % with |t| ≤ 1.04. Too few independent days support it to count.
- **F3:** The book barely traded and lost on its trades. The choppy-agitated regime covered 4.6 % of bars, and the 173 short trades averaged -4.40 % after fees (median -3.38 %, held 10.2 days). The book's mean daily return stayed between -0.06 % and +0.10 % in every window from w7 to w18.
- **F4:** The largest one-day falls are followed by a next-day rebound. The bottom decile of z-scored daily returns gains +1.43 % the next day (983 bars, unclustered t 6.29). Clustered by day, it holds mainly in falling agitated markets (+2.44 %, 164 cases on 54 days, t 2.16) and rising calm markets (+2.01 %, 70 cases on 39 days, t 2.61), and is weaker elsewhere (|t| ≤ 1.44). Falling-agitated rebounds are already held, 16 strategies in that cell.
- **F5:** Closes near the day's low are followed by a next-day gain. The lowest fifth of close positions gains +0.66 % the next day (1,965 bars, unclustered t 5.13). By profile, only falling agitated stands out (+2.27 %, 203 cases on 91 days, t 2.29). This repeats the agitated low-close rebounds the map already holds (039-02, 045-01).
- **F6:** The Thursday and Friday next-day gains are coins moving together, not separate evidence. Unclustered, they reach +0.51 % (t 3.60) and +0.54 % (t 4.11), but with the cases of one day taken together the t falls to 1.07 and 1.50. Within profiles, rising calm reaches t 3.01 (already held as 045-01, rising market late week gain) and choppy calm reaches t 2.50 (141 cases on 79 days).

## Ideas
- No ideas: Across about fifty profile-by-pattern cells, nothing new reaches the bar that many looks require. The only clustered t values above 2.5 repeat strategies the map already holds (falling-agitated rebounds, low-close rebounds, the rising late-week gain). The rest are marginal (rising-calm fall rebound t 2.61, choppy-calm late week t 2.50) or rest on fewer than 10 independent days (choppy deep-slide continuation, F2).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
