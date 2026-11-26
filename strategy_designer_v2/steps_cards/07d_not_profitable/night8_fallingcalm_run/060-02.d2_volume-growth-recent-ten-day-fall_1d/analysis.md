---
line: 7.d confirmed, not profitable
backtest: 060-02.d2_volume-growth-recent-ten-day-fall_1d
idea tested: 060-02.d2_volume-growth-recent-ten-day-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4572 USD
---
## Findings
- **F1:** The book's deepest fall, -22.4 % over 16 days inside w14, came entirely from long positions. The long side summed -0.243 and the short side 0.000, against -0.371 for holding the coins. All six coins were long: BTC -0.224, ETH -0.282, LTC -0.238, XMR -0.367, XRP -0.111 and ZEC -0.240. They were entered on growing-volume signals while the coins' 10-day returns were -13 % to -19 % and their 20-day daily swing was 4.98 % to 8.07 %, so the book was buying a still-running crash.
- **F2:** The two sides differ in both gain and falls. The short side (volume shrinking, the brief's own continuation) earned a mean 0.036 % a day against 0.018 % for the long side. Rebuilt before fees from the positions, the short side alone has a deepest fall of -13.9 % and a Calmar of 0.96. The long side alone has -22.5 % and 0.25, against -22.3 % and 0.89 for the whole book. The long side carries the failing Calmar.
- **F3:** The gain depends on how deep the 10-day fall is.
- **F4:** Condition check: the deep-fall condition alone earns about half of what it earns with growing volume. Taking all signal cases of the deepest tercile, either side, the 5-day return is +2.58 % (t 2.21, 138 cases), against +5.14 % for those with growing volume. In the mildest tercile all signal cases give +0.34 % (t 0.34, 176 cases), so mildness alone carries no effect. Growing volume adds a rise beyond the deep fall itself, which is the brief's own reading: growing volume in a fall is capitulation, where the fall stalls.
- **F5:** Tying each side to its part of the fall repairs the falls, rebuilt before fees.
- **F6:** Cost is not what fails. The total move per case (+1.35 %) is 7.0 times the 0.19 % a trade costs, and the book's Sharpe (0.76) beats holding by 0.21. Only the depth of its long-side falls fails.

## Ideas
- `060-02.d2.d1_volume-dry-up-short-only` (from F1, F2, F6): In a falling market, while the coin's 10-day return is still negative, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.
- `060-02.d2.d2_volume-growth-capitulation-rebound` (from F1, F3, F4, F5): In a falling market, the more the coin's trading volume over the past 30 days has grown against the 30 days before, the larger its rise over the next 5 days, and the deeper its 10-day fall has been, the larger that rise.
- `060-02.d2.d3_dry-up-in-moderate-declines` (from F2, F3, F5): In a falling market, while the coin's 10-day return is negative but its fall is still moderate, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
