---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3195 USD
---
## Findings
- **F1:** Per signal, the book captures less than one round trip costs, so it cannot pay. The idea's move per case is +0.15 % over 1 day, 0.9 times the 0.16 % cost. The book's mean gain before fees was 0.006 % per bar on BTC and 0.041 % on ETH, against fees of 0.037 % and 0.035 % per bar. Turnover was 0.38 to 0.50 of the book per bar. Its daily return was -0.032 % on BTC and +0.006 % on ETH, against +0.118 % and +0.137 % for holding.
- **F2:** The short half loses outright. On bars with a negative forecast the position earned -0.028 % per bar before fees and paid 0.036 % in fees (2962 bars). That is because the coin's raw next-day return there was still +0.018 % against a drift of about +0.12 % a day. The long half earned +0.077 % per bar before 0.037 % of fees (2832 bars).
- **F3:** After a large vol-scaled rise the coin keeps rising rather than giving back. Over all regimes, after a 1-day rise of more than one 20-day usual move the next day ends 0.22 % above drift (t 1.6, 762 cases). After a 5-day rise of more than one usual 5-day move the coin keeps rising: 0.43 % above drift over 1 day (t 3.4, 902 cases), 0.80 % over 2 days (t 3.2, 450 cases), and 1.55 % over 3 days (t 4.1, 296 cases, strength 0.23). The 3-day continuation is about 10 times the cost.
- **F4:** The reversal holds only against the coin's slower trend, and there it is several times the cost.
- **F5:** The rebound after a large vol-scaled 1-day fall grows with the horizon, but the evidence is weak. Over all cases it is 0.35 % above drift over 1 day (t 1.9, 657 cases), 0.84 % over 5 days (t 1.2, 147 cases) and 1.79 % over 10 days (t 1.4, 83 cases).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend` (from F1, F2, F4): The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day, only while its close is above its 50-day average. The larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its close is below its 50-day average.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going` (from F1, F3): The larger a coin's 5-day return relative to its own 20-day daily volatility, the more it keeps rising over the next 3 days.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls` (from F1, F5): The larger a coin's 1-day fall relative to its own 20-day daily volatility, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
