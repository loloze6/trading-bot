---
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
idea tested: N2-02_capitulation-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2945 USD
---
## Findings
- **F1:** The pooled result rests on a few large winners. After forecast ≥ 10, the mean 10-bar excess is +0.021 (t 0.90, 69 non-overlapping cases), but the median is −0.016 and only 48% of cases are positive. Dropping the 5% largest absolute moves brings the mean to −0.0005 (t −0.03, 65 cases), and XRP alone averages +0.119 with a median of −0.019 (11 cases).
- **F2:** When the coin was still falling into the signal, the rebound is concentrated there. Top-forecast bars with a negative 3-day return average +0.043 excess (median +0.006, 55% positive, t 1.27, 42 cases). Those with a positive 3-day return average −0.014 (37% positive, t −0.51, 27 cases). The 5-day split gives the same picture: +0.036 (t 1.26, 50 cases) against −0.019 (19 cases).
- **F3:** The same split holds in the deepest fifth of in-regime distance below the 200-day SMA, and it shows up in both directions. A negative 3-day return gives +0.028 excess (t 1.32, 76 cases). A positive 3-day return, meaning the bounce has already started, gives −0.034 (35% positive, t −2.38, 83 cases).
- **F4:** The market's own moves drown the effect. Top-forecast 10-bar returns correlate 0.80 with the cross-coin mean return over the same 10 bars. Subtracting that mean cuts the standard deviation from 0.19 to 0.12 and raises the t from 0.90 to 1.40 (mean +0.021, 64 cases).
- **F5:** One period dominates the cases and drags the result down. 2022 holds 32 of the 69 top-forecast cases (28 of them in window w2), averaging −0.019 excess with 38% positive (t −0.76). Most other years are positive, for example 2024 at +0.105 (t 2.03, 6 cases) and 2020 at +0.059 (4 cases).
- **F6:** Depth alone does not sort outcomes inside the high-volatility regime. All five quintiles of distance from the 200-day SMA have mean excess between −0.009 and 0.000, with |t| ≤ 0.53 and 159 cases each.

## Ideas
- `N2-02_capitulation-rebound.b1_still-falling-deep-capitulation-rebound` (from F2, F3, F1): When a coin's daily close is far below its 200-day average in a high-volatility stretch and it has still fallen over the last three days, it rises more than its usual drift over the next ten days.
- `N2-02_capitulation-rebound.b2_early-bounce-fades-below-trend` (from F3, F2): When a coin's daily close is far below its 200-day average in a high-volatility stretch but it has risen over the last three days, it falls back below its usual drift over the next ten days.
- `N2-02_capitulation-rebound.b3_capitulated-coin-beats-market` (from F4, F2): When a coin's daily close is far below its 200-day average in a high-volatility stretch and it fell over the last three days, it outperforms the average of the other coins over the next ten days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
