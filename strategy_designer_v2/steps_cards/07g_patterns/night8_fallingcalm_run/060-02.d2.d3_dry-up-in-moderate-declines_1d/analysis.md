---
line: 7.g patterns
backtest: 060-02.d2.d3_dry-up-in-moderate-declines_1d
idea tested: 060-02.d2.d3_dry-up-in-moderate-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5925 USD
---
## Findings
- **F1:** In the falling profile (60-day return below -10 %), the 147 grid bars where the book was short (forecast below 0) were followed by a 5-day excess return of -3.71 % (cluster t -2.24, 48 days), while the 254 falling-market grid bars with no signal were followed by +1.34 % (t 0.96, 79 days); the short signal picks out the falling-market bars that keep falling.
- **F2:** In falling markets, how far the coin keeps falling depends on how deep its 10-day fall already is, and the link is not straight. Grid bars with a moderate 10-day fall (quintile mean -4.8 %) were followed by -3.38 % excess (cluster t -2.79, 78 cases, 39 days). Those with a deep fall (mean -26 %) were followed by +0.80 % (t 0.26), and those with a 10-day rise (mean +20 %) by +2.61 % (t 1.38). The fall extends in the middle of a decline, not after a crash.
- **F3:** In falling markets, volume shrinkage grades the fall over all 401 grid bars. The most-shrunk quartile was followed by -3.02 % excess (t -2.66, 103 cases), against +0.46 % in the least-shrunk quartile. The Spearman rho of shrinkage with excess return is -0.099 (p 0.048). In an OLS with close location and 10-day return held fixed, the shrinkage slope is -0.024 per log unit (t -2.54), while the 10-day return adds nothing linearly (t 0.17).
- **F4:** The strongest volume shrinkage in falling markets happens when the coin is calm. In the lowest and middle agitation terciles, the most-shrunk quartile fell -3.01 % (t -1.98, 68 cases) and -3.05 % (t -1.90, 35 cases). The most agitated tercile has no case in that quartile.
- **F5:** The short signal's continuation comes from the grinding bear years. It was -5.81 % in 2018 (t -3.83, 64 cases) and -3.53 % in 2019 (t -3.23, 49 cases). It reversed to +4.49 % in 2020 (11 cases, crash rebound) and was -2.15 % in 2021 (t -0.89).
- **F6:** Other patterns did not stand out once they were clustered by day.

## Ideas
- `060-02.d2.d3.g1_calm-falling-volume-dry-up` (from F1, F3, F4, F5): In a falling, calm market, the more the coin's mean daily volume over the past 30 days has shrunk against the 30 days before, the further it falls over the next 5 days.
- `060-02.d2.d3.g2_dry-up-short-mid-decline` (from F1, F2, F3): In a falling market, the more the coin's mean daily volume over the past 30 days has shrunk against the 30 days before, the further it falls over the next 5 days. The effect is largest when its 10-day return shows a moderate decline rather than a crash.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
