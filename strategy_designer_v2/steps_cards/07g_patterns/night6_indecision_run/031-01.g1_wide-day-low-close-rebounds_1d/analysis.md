---
line: 7.g patterns
backtest: 031-01.g1_wide-day-low-close-rebounds_1d
idea tested: 031-01.g1_wide-day-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4077 USD
---
## Findings
- **F1:** Across all days that close in the bottom quarter of their range, the next-day return above the coin's mean rises with the day's range as a share of its close, by per-coin quintile: −0.07 % (t −0.38, 704 cases), −0.28 %, +0.05 %, +0.49 % (t 1.72), then +1.45 % in the top quintile (t 3.77, 711 cases, 332 days). The size of the range in price terms grades the rebound, not only the range against its 20-day mean.
- **F2:** Among the tested situation's own days (range ≥ 1.5× its 20-day mean, close in the bottom quarter), the next-day excess return depends on volatility. By the coin's 20-day volatility tercile it is −0.13 % (t −0.30, 178 cases), +0.64 % (t 1.54), then +3.30 % in the top tercile (t 3.52, 160 cases, 99 days). By range-to-close quartile it is −0.17 %, +0.80 %, +1.14 %, then +2.99 % (t 2.39, 132 cases).
- **F3:** After a prior 5-day fall (5-day return z < −0.5, the day excluded), a day closing in the top quarter of its range is followed by a below-mean next day. This holds at every range level: −0.77 % (t −3.14, 704 cases, 408 days) for ranges under the 20-day mean, −0.80 % (t −2.31) for 1–1.5×, and −2.27 % (t −2.39, 66 cases) above 2×.
- **F4:** On wide days (≥ 1.5×) that close near the high, the next-day excess return deepens as the prior 5-day fall deepens. By prior 5-day z it is +0.26 % (z > 1.5), −0.21 %, +0.06 %, −0.67 % (t −1.37), then −2.55 % for z < −1.5 (t −2.28, 61 cases, 36 days). It is negative on all 6 coins after a fall, from −0.68 % to −2.36 % (ETH t −2.92).
- **F5:** The book's in-position bars average +1.00 % (608 bars), and the top 10 % of those bars carry 106 % of its total gain. By the coin's volatility tercile the in-position bar mean is +0.02 %, +0.67 %, then +2.07 %, so the book earns almost only when the coin is volatile.
- **F6:** The tested rebound is uneven across years: from +0.10 % (2024, t 0.11) to +3.28 % (2020, t 1.87), with no year above t 2. The whole effect rests on pooling the years and on the volatile cases above.

## Ideas
- `031-01.g1.g1_large-range-low-close-rebounds` (from F1, F2): After a day that closes near its low, the coin rises over the next 1 day. The wider that day's high-low range as a share of its closing price, the larger the rise.
- `031-01.g1.g2_volatility-scales-wide-low-rebound` (from F2, F5): On a day whose range is wide against its 20-day average and whose close lands near its low, the next-day rise is larger the higher the coin's 20-day volatility of daily returns.
- `031-01.g1.g3_high-close-in-downtrend-fades` (from F3, F4): After a coin has fallen over the past 5 days, a day that closes near its high is followed by a fall over the next 1 day. The deeper the 5-day fall and the nearer the close to the day's high, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
