---
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3510 USD
---
## Findings
- **F1:** Step 5's main measure sits on the side the idea predicts but short of the bar: +0.21 % excess over 18 bars, t 1.63, on 4437 cases. Re-counted on each cell's first bet bar, the same move is +0.29 % (t 2.18, 4444 cases), +0.19 % at 12 bars (t 1.81) and +0.04 % at 6 bars (t 0.49). The effect is small (strength 0.024 to 0.032), not absent.
- **F2:** The effect is not graded by the forecast. Spearman between forecast and excess return is -0.014 in step 5 and -0.004 here. By forecast quartile (mean forecast 3.4, 9.3, 19.4, 20.0) the excess return is +0.38 %, +0.24 %, +0.08 % and +0.45 %, with no rise. That alone keeps the plan's confirm rule out of reach, whatever the t.
- **F3:** The market's own moves drown the effect. By year, the excess return against the all-window drift swings from -1.31 % (2018, t -2.98) and -0.74 % (2022, t -2.01) to +1.03 % (2020, t 2.63) and +1.85 % (2021, t 3.58). Against each window's own drift, every year except 2021 (+1.25 %, t 2.48) sits between -0.04 % and +0.72 % with |t| < 1.9. Signal cells beat non-signal cells by only +0.28 % (Welch t 1.34; 4444 against 1267 cases).
- **F4:** The rise is concentrated in surges that come with a large one-day move, in either direction:
- **F5:** The effect is spread thinly across coins and leans toward rising markets:
- **F6:** Per case the total move (+0.62 %) is 3.2 times the 0.19 % cost of a trade, and the unusual move (+0.21 %) is 1.1 times that cost. The book's Sharpe is 0.81 but its Calmar is 0.56. The large-move cases in F4 (+1.33 %) would cover the cost about seven times.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins` (from F1, F5): When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days. The higher the volume against that average, the larger the rise.
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b2_surge-on-big-move-rises` (from F4, F2, F6): When a coin trades a four-hour volume far above its 30-day average while its 1-day return is large in either direction, it rises over the next three days. The larger the absolute size of that 1-day move on the volume surge, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
