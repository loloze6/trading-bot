---
line: 7.g patterns
backtest: 003-03_heavy-volume-rise-continues_1d
idea tested: 003-03_heavy-volume-rise-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4923 USD
---
## Findings
- **F1:** The continuation after heavy-volume rises arrives late. On up days in each coin's top quintile of (one-day return over its 20-day standard deviation) × (volume over its 30-day mean), the next-day excess return is -0.0031 (t -0.78, n 248), while the excess return from day 1 to day 6 is +0.0268 (t 3.70, n 248). That later return rises steadily across the quintiles: -0.0029, -0.0014, +0.0019, +0.0090, +0.0268. Its Spearman with the score is 0.080 (p 0.005), against 0.006 (p 0.83) for the next day alone.
- **F2:** The book sells out before that later drift arrives. After a top-quintile event its absolute allocation is 0.20 one bar later and 0.13 three bars later, and it earns 0.0013 on the event day against 0.0039 summed over days 1 to 4. Its mean daily return per coin lies between -0.00044 and +0.00048, while holding earns between 0.00067 and 0.00155.
- **F3:** Volume separates what follows the largest rises. On the 5-day grid, top-z days in the heavy-volume tercile are followed by an excess of +0.0219 (t 3.10, n 296), against +0.0101 (t 0.80, n 77) in the light tercile. The largest falls show the brief's ordering only weakly: -0.0149 after light volume (t -1.33, n 70) against +0.0003 after heavy volume (t 0.05, n 277), which cannot be told apart from chance.
- **F4:** The heavy-rise excess on forecast >= 2 grid bars is negative in the two falling years and positive in the other six. It is -0.0277 (t -1.73, n 52) in 2018 and -0.0149 (t -1.36, n 60) in 2022, against +0.016 to +0.058 elsewhere (2021: t 3.03, n 67). This suggests a bear-market regime limits the continuation, though two years are too few to support an idea.
- **F5:** Past trend alone predicts nothing on the 5-day grid. The Spearman of the 5-day excess with the 5-day past return is -0.017 (p 0.32), and with the 20-day past return 0.013 (p 0.50), so the effect in F1 belongs to the volume-weighted one-day move, not to momentum.
- **F6:** Thursday and Friday next-day excess returns exceed the other weekdays in all six coins, from +0.0010 in BTC (t 0.78) to +0.0076 in LTC (t 3.88). However, the cross-coin Friday mean is +0.0032 with only t 2.17 (n 414), and the gap fades after 2019 (2018-2019 t 1.66 and 2.72; 2020-2025 all |t| < 0.91). After this many angles that is not separable from chance.

## Ideas
- `003-03_heavy-volume-rise-continues.g1_delayed-heavy-volume-rise-drift` (from F1, F2, F3, F5): When a coin rises over one day by a large multiple of its usual 20-day daily move on volume above its 30-day average daily volume, it rises more than usual over the five days that begin one day after the rise, and not on the next day itself. The larger the rise in usual moves times its volume ratio, the larger that later gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
