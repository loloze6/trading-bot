---
line: 7.b inconclusive
backtest: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high_1d
idea tested: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3544 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: step 5 found a slope t of +1.47 on 327 grid cases with top-minus-bottom third +1.9 %, and on folds B and C alone I get t +1.42 on 151 cases with top-minus-bottom +3.1 %, so the problem is too few cases for an effect this weak, not an effect on the other side.
- **F2:** The effect is weak and partly depends on which grid is used: across the 5 possible start offsets of the 5-day grid the slope t averages +0.72 (range −0.09 to +1.42), and on 10-day and 20-day grids it averages +0.79 and +0.69, so the plan's grid (t +1.42) is the most favourable draw.
- **F3:** The gain sits mostly in compression versus expansion, not in a gradient inside compression: compressed cases (forecast > 0) show a 5-day excess of +6.55 % (day-clustered t 2.81, 84 cases on 43 days) against +0.34 % for expanded ones (t 0.15, 67 cases on 46 days), while within compressed cases the slope t averages −0.93 across offsets and forecast quintiles 2 to 4 give +8.8 %, +4.9 % and +4.1 %.
- **F4:** Closes at the 28-day high in general are followed by excess gains, which lifts every group: the trending-grid 5-day excess averages +1.9 % across offsets (mean t 1.68), against −0.25 % on the other bars, so the market's own breakout drift outweighs the compression gradient.
- **F5:** The effect is uneven across coins and years: the 5-day slope t is +2.04 for ZEC and +1.46 for ETH but −0.66 for XRP (top-minus-bottom −24.8 %, mean excess +14.3 % carried by a few cases), and by year it is +2.39 in 2021 but between −0.98 and +0.44 in 2018 to 2020.
- **F6:** Per case the idea is too small to pay at this sample: step 5 sizes the unusual move at +0.18 % (t 0.34, 494 days, strength 0.026), and the total move of +0.24 % is only 1.2 times the 0.19 % cost of a trade, which matches the book's Sharpe of −0.06.

## Ideas
- `032-02.g1.e1.e2.b1_quiet-breakout-all-coins` (from F1, F2, F5): Among coins closing near their highest close of the last 28 days, the quieter the coin's daily returns over the last 20 days compared with the last 60 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
