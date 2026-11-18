---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.g patterns
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a sharp daily fall on volume below the coin's own 30-day average, the coin keeps falling over the next 3 days. The lighter the volume relative to that average, the larger the further fall.
Consequence: A quiet sharp fall is a reason to stay out of, or lean short on, the coin for the next 3 days, rather than to buy the dip.
Why:
- F2: Among sharp falls (z < −1, n 623), the 3-day excess return rises with the volume ratio. The Spearman correlation is 0.133 (p 0.0008). The low-volume tercile gives −0.0137 (t −2.24, n 208) and the high-volume tercile gives +0.0256 (t 3.52, n 208).
- F3: The lower wick adds nothing and points the wrong way. Its Spearman correlation with the excess return among sharp falls is −0.066. In every volume tercile, falls with a long wick did worse than falls with a short wick: low volume −0.0247 (t −2.45) vs −0.0062, mid volume −0.0133 vs +0.0064, high volume +0.0226 vs +0.0303.
- F4: Quiet sharp falls tend to continue lower in most coins. Low-volume falls returned −0.033 in LTC (t −2.15), −0.035 in XRP (t −2.16) and −0.025 in ZEC (t −1.65). High-volume falls were positive in all six coins, and positive in every year from 2020 to 2025 (+0.019 to +0.067). They were negative in 2018 (−0.015) and 2019 (−0.003).
