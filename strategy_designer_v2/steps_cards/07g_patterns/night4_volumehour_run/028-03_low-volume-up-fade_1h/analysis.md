---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade_1h
idea tested: 028-03_low-volume-up-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3719 USD
---
## Findings
- **F1:** Two UTC hours stand out in every hourly bar of both coins. Excess one-hour returns are +4.49 bp (t 4.00) on the 20:00 bar and +4.04 bp (t 3.69) on the 21:00 bar, about 5,836 bars each. No other hour of the 24 reaches |t| 3.4. Measured from the 19:00 close over those two bars, the stretch is +3.55 bp (t 1.85, 2,918 days) on BTC and +5.12 bp (t 2.09, 2,918 days) on ETH. It is positive in 32 of 48 coin-windows (0.67) and in 6 of 8 years, with 2020 at +15.89 bp (t 3.95) and 2021 at +12.12 bp (t 2.28).
- **F2:** The evening rise is graded by the coin's own 24-hour return up to the 19:00 close, scaled by its usual hourly move. From the weakest to the strongest quintile it falls steadily: +16.70 bp (t 3.22, n 1,072), +7.26 bp (t 2.05), −0.86 bp, −3.48 bp and −2.22 bp. So the evening lift belongs to days that had been falling.
- **F3:** The tested fade does not show at any size of the hour inside its volume band (0.5 to 1.5 times the 720-bar mean). The signed 6-bar move per bucket of the hour's size in usual moves is +2.16 bp (t 0.83, n 5,443) for 0–1, +0.09 bp for 1–2, −2.20 bp (t −0.28) for 2–3 and −25.92 bp (t −1.62, n 208) for 3–5. This matches step 5's strength of 0.011 and its failed size check (−0.0018 %).
- **F4:** The book lost from timing and costs, not just from shorting a rising market. It averaged −19.75 bp a day on BTC and −16.72 bp on ETH, while the coins rose +11.83 and +13.68 bp. The average position of −0.46 accounts for only −6.26 and −5.32 bp a day. Its 19,983 trades, all short and lasting 8.7 hours on average, lost −0.33 % each before fees and −0.43 % after. Its daily returns correlate −0.65 with the coin's.
- **F5:** Two more patterns are not strong enough to count after this many angles. The early UTC hours are weak: 00:00 to 02:00 show −2.25 bp, −2.31 bp and −3.18 bp (t −3.35). Yet the 3-hour stretch from the 23:00 close is only −3.36 bp (t −1.50) on BTC and −3.45 bp (t −1.12) on ETH, with no steady sign across years. Small down-hours (under one usual move) are followed by a further 6-bar fall of 6.16 bp (t 2.90, n 7,199). That is one cell out of about twenty tested and has no grading.

## Ideas
- `028-03_low-volume-up-fade.g1_evening-rebound-after-down-days` (from F1, F2): Over the two hours from 20:00 to 22:00 UTC, the coin rises more than its normal drift. The further it has fallen over the past 24 hours, measured in its usual hourly moves, the larger that evening rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
