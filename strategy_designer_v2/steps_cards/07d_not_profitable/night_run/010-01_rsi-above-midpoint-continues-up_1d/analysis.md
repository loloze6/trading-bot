---
line: 7.d not profitable
backtest: 010-01_rsi-above-midpoint-continues-up_1d
idea tested: 010-01_rsi-above-midpoint-continues-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2974 USD
---
## Findings
- **F1:** The book's Calmar of 0.47 comes from one deep fall, not from a lack of gain. Its yearly return is 28.8%, but its deepest fall is -61.8%. That fall lasted 1,089 days and bottomed in w5. The next deepest falls were -46.2% (486 days, bottom in w21) and -32.7% (bottom in w1).
- **F2:** The short side earns nothing, and that is where the losses sit. Short days average +0.000023 a day (t 0.05, n 2,784). Long days average +0.001904 (t 3.81, n 2,801).
- **F3:** The shorts do read timing, but they fight the coin's own rise. Their timing gain is +0.000834 a day. Their market part is -0.000762 a day, because both coins rose on average (BTC +0.00118 and ETH +0.00137 a day). So the shorts net to about zero.
- **F4:** Inside the two deepest falls, the shorts carried the losses while the longs gained. In the -61.8% fall, short days summed -1.28 against +1.78 for long days. In the -46.2% fall, short days summed -0.19 against +0.39 for long days.
- **F5:** The short losses come in clusters by year. Short days summed -0.77 in 2023 and -0.74 in 2024. They summed +0.52 in 2018, +0.51 in 2022 and +0.78 in 2025.
- **F6:** Going long-only fixes the failed measure. Keeping only the long days raises Calmar from 0.47 to 0.91 and cuts the deepest fall from -61.8% to -36.3%. The yearly return rises from 28.8% to 33.1% and Sharpe from 0.82 to 1.06.
- **F7:** Simple trend filters on the shorts do not help. Flattening the shorts when the 90-day return was positive lowers Calmar to 0.35. Flattening both sides against the 90-day trend gives 0.36. In fact, shorts taken while the 90-day return was positive averaged +0.0038 a day (n 196).

## Ideas
- `010-01_rsi-above-midpoint-continues-up.d1_rsi-above-share-long-side-only` (from F1, F2, F3, F4, F6, F7): The larger the share of the past 14 days that a coin's 14-day RSI has spent above its midpoint, the larger the coin's rise over the next 7 days, only while that share is more than half. When RSI has sat mostly below its midpoint, the coin's next 7 days follow its ordinary upward drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
