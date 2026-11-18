---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.g patterns
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises over one day by a large multiple of its usual 20-day daily move on volume above its 30-day average daily volume, it rises more than usual over the five days that begin one day after the rise, and not on the next day itself. The larger the rise in usual moves times its volume ratio, the larger that later gain.
Consequence: A trader buying a heavy-volume rise should hold it for about a week, because the gain comes on days 2 to 6 rather than on the next day.
Why:
- F1: The continuation after heavy-volume rises arrives late. On up days in each coin's top quintile of (one-day return over its 20-day standard deviation) × (volume over its 30-day mean), the next-day excess return is -0.0031 (t -0.78, n 248), while the excess return from day 1 to day 6 is +0.0268 (t 3.70, n 248). That later return rises steadily across the quintiles: -0.0029, -0.0014, +0.0019, +0.0090, +0.0268. Its Spearman with the score is 0.080 (p 0.005), against 0.006 (p 0.83) for the next day alone.
- F2: The book sells out before that later drift arrives. After a top-quintile event its absolute allocation is 0.20 one bar later and 0.13 three bars later, and it earns 0.0013 on the event day against 0.0039 summed over days 1 to 4. Its mean daily return per coin lies between -0.00044 and +0.00048, while holding earns between 0.00067 and 0.00155.
- F3: Volume separates what follows the largest rises. On the 5-day grid, top-z days in the heavy-volume tercile are followed by an excess of +0.0219 (t 3.10, n 296), against +0.0101 (t 0.80, n 77) in the light tercile. The largest falls show the brief's ordering only weakly: -0.0149 after light volume (t -1.33, n 70) against +0.0003 after heavy volume (t 0.05, n 277), which cannot be told apart from chance.
- F5: Past trend alone predicts nothing on the 5-day grid. The Spearman of the 5-day excess with the 5-day past return is -0.017 (p 0.32), and with the 20-day past return 0.013 (p 0.50), so the effect in F1 belongs to the volume-weighted one-day move, not to momentum.
