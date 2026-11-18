---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.g patterns
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a day on which a coin closes lower, its return over the next 3 days is higher the larger that day's volume is relative to the coin's own 30-day average volume. It turns negative after falls on light volume, whatever the lower wick.
Consequence: A trader would buy a down day only when it came on a heavy volume burst, sizing up with the burst, and would refuse to buy quiet falls or long-wick falls on light volume.
Why:
- F1: Volume alone carries the rebound after a fall. On the non-overlapping 3-day grid, down days (1-day return below 0) in the top volume-ratio quintile were followed by a mean 3-day excess return of +0.0180 (t 3.88, n 491). The other four quintiles were all negative, from −0.0013 to −0.0055 (|t| ≤ 1.49).
- F2: Among sharp falls (z < −1, n 623), the 3-day excess return rises with the volume ratio. The Spearman correlation is 0.133 (p 0.0008). The low-volume tercile gives −0.0137 (t −2.24, n 208) and the high-volume tercile gives +0.0256 (t 3.52, n 208).
- F3: The lower wick adds nothing and points the wrong way. Its Spearman correlation with the excess return among sharp falls is −0.066. In every volume tercile, falls with a long wick did worse than falls with a short wick: low volume −0.0247 (t −2.45) vs −0.0062, mid volume −0.0133 vs +0.0064, high volume +0.0226 vs +0.0303.
- F5: The volume effect is one-sided. Up days in the top volume-ratio quintile gave only +0.0008 (t 0.22, n 538), against +0.0180 for down days in the same quintile.
- F7: The book barely beats holding. Its Sharpe is 0.557, only 0.003 above holding's Sharpe. Its mean daily return is +0.0004, and 2018 and 2022 were negative. The per-coin forecast ≥ 2 rebound was near zero in BTC (+0.0003) and ETH (+0.0015), and largest in ZEC (+0.029, t 2.74) and LTC (+0.015, t 2.09).
