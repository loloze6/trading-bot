---
line: 7.b inconclusive
backtest: 067-02.b1.b1_two-sided-swing-stretch-five-days_1d
idea tested: 067-02.b1.b1_two-sided-swing-stretch-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3570 USD
---
## Findings
- **F1:** In folds B and C, on the 5-day grid, the tested effect shows on one side only. Closes below the 20-day average were followed by further fall: the short side's signed excess 5-day return was +2.68 % (t 3.29, 145 cases). Closes above the average were followed by nothing: the long side's was −0.19 % (t −0.21, 142 cases). This matches step 5's failed supporting check, whose weaker side was at −0.53 %.
- **F2:** The short side's carry is concentrated in agitated markets. With the 30-day swing above the coin's median, the signed excess was +5.41 % (t 3.86, 66 cases). In calm markets it was +0.40 % (t 0.47, 79 cases). The long side was flat in both: −0.89 % (t −0.48, 42 cases) agitated and +0.11 % (t 0.10, 100 cases) calm.
- **F3:** By raw stretch, the deepest-below sextile (stretch −4.5 to −2.0 usual moves) had a 5-day excess of −4.51 % (t −2.44, 48 cases). The highest-above sextile (stretch +2.5 to +7.2) had only +1.47 % (t 0.72, 48 cases), and every sextile below +0.85 was negative. Below the average, the move follows the stretch in its direction; above it, the effect is not distinguishable from zero.
- **F4:** The grading inside the short side is not clean. By forecast size, the short side's third quartile had a signed excess of +6.15 % (t 3.28, 44 cases), but the largest quartile had −0.35 % (t −0.21, 22 cases). The strongest shorts are not the largest forecasts.
- **F5:** Part of the mixed result is the market's own path, by year:
- **F6:** The 5-day horizon is where the effect is clearest; neither shorter nor longer horizons do better. In folds B and C the forecast slope's t was:
- **F7:** The pooled idea is too small to pay, but its strong part is not. Its total move per case is +0.23 %, against a trade cost of 0.19 % (1.2 times), with a strength of 0.018. The short side in agitated markets carries +5.41 % per 5-day case, about 28 times the cost.

## Ideas
- `067-02.b1.b1.b1_agitated-chop-downside-stretch-carries` (from F1, F2, F3, F6, F7): In a choppy, agitated market, the further a coin's close stands below its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.
- `067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling` (from F1, F3, F5, F6): In a choppy market, the further a coin's close stands below its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
