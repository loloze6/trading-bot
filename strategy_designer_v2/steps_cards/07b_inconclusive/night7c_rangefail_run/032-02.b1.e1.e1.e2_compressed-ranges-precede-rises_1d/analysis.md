---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d
idea tested: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3421 USD
---
## Findings
- **F1:** Compression alone does not predict the coin's rise. At 20 days the plan's forecast has a correlation of 0.036 with the excess return (t 0.73, 414 grid cases), and the raw narrowness (−W) has 0.096 (t 1.35, 198 cases). At 5, 10 and 40 days |t| stays under 1.4. The 20-day excess return by forecast fifth does not rise in order: −3.0 %, −2.2 %, +5.9 %, −1.5 %, +0.8 %.
- **F2:** Compression does predict a move once it is signed by where the close sits in its 60-day range (position from the middle over the range, divided by W). At 10 days this has a correlation of 0.193 (t 3.99, 414 cases) and its fifths rise in order: −3.3 %, −3.7 %, −0.7 %, +1.8 %, +6.4 %. At 20 days the correlation is 0.198 (t 2.83, 198 cases), with the top fifth at +13.5 % against the bottom fifth at −3.2 %.
- **F3:** Compression grades this directional effect. Position in the range alone gives t 3.57 at 10 days, and its slope is largest in the tightest third of ranges (corr 0.245, t 2.95). It is weaker in the middle third (t 1.46) and the widest third (t 1.16). Tight ranges also have the largest mean absolute 20-day move (21.5 % against 19.0 % for wide).
- **F4:** The directional effect is not even across the data. At 10 days the t is 4.79 in 2019, 2.41 in 2020, 0.23 in 2021 and −1.46 in 2018. By coin it is 3.10 for XRP, 2.17 for ETH, 1.99 for XMR, 1.68 for ZEC, 0.88 for LTC and 0.00 for BTC.
- **F5:** The brief's fade of closes beyond the range edge does not appear. At 10 days the 45 grid cases with a close past the edge have a signed excess return of +0.8 % in the break's direction (t 0.23). At 20 days the 26 such cases have −4.7 % (t −0.68). Neither can be told from zero.
- **F6:** The test measured the effect where it does not show. The plan's long-only forecast correlates only 0.21 with the signed compression measure, so its slope (t 0.11) averaged up-moves and down-moves out of compressed ranges together. That is why the result is unclear.

## Ideas
- `032-02.b1.e1.e1.e2.b1_compressed-range-resolves-toward-close` (from F1, F2, F3, F5, F6): The narrower a coin's 60-day range of closes is against its average absolute daily move, the larger its move over the next 10 days in the direction of its latest close's place from the middle of that range: up when the close sits in the upper part, down when it sits in the lower part.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
