---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4968 USD
---
## Findings
- **F1:** In the high-volatility regime (20-day volatility rank over 100 days ≥ 0.8), the next day's excess return falls with the day's move over its 60-day mean absolute move: slope −0.0034 (t −3.28, n 542) in BTC and −0.0058 (t −4.02, n 498) in ETH. Outside the regime the slope is flat (t −0.09 and −0.08, n 1851 and 1895).
- **F2:** The fade in the high-volatility regime lasts about 3 days, then fades out. The 3-day slopes on the move ratio are −0.0064 (t −2.47, n 181) in BTC and −0.0131 (t −3.75, n 167) in ETH. By 5 days they shrink to t −0.82 and −0.84 (n 101, 94). Outside the regime the 3-day slopes are slightly positive (t 0.32 and 1.57).
- **F3:** In the high-volatility regime, the reversal after down days is fast and the reversal after up days is slow. After down days, the slope of excess return on the size of the move is +0.0059 at 1 day (t 2.93, n 517) and +0.0107 at 3 days (t 2.05, n 157). After up days it is only −0.0023 at 1 day (t −1.44, n 523) but −0.0100 at 3 days (t −2.83, n 191).
- **F4:** The book's trades earn on quick turns and lose when held. Trades held ≤1.5 days average +1.86% net (n 597). Trades held 1.5–3.5 days average −1.77% (n 232), and 3.5–7.5 days −5.25% (n 80). BTC shorts lose −0.75% per trade (n 244) while BTC longs gain +0.63% (n 240).
- **F5:** Large down days outside the regime (ratio ≤ −2) are followed by a +0.94% next-day excess return (t 2.35, n 152), but the sign changes by year. It is −1.05% in 2019, −1.25% in 2022 and −1.84% in 2024, so it does not stand out from chance.
- **F6:** The book's next-day return is highest after its own extreme days: +0.00305 after its worst decile and +0.00197 after its best, against about 0 in the middle deciles. Its day-to-day autocorrelation has opposite signs in the two coins (BTC +0.10, ETH −0.11), so this is volatility clustering rather than direction. No weekday effect stands out on the coins' next-day excess returns: every |t| is ≤ 1.58.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound` (from F1, F3, F4): In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day fall is followed by a rebound over the next day. The larger the fall relative to the coin's 60-day mean absolute daily move, the larger that next-day rise.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g2_volatile-rise-slow-giveback` (from F2, F3): In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day rise gives back slowly, over the next 3 days rather than the next day. The larger the rise relative to the coin's 60-day mean absolute daily move, the larger the fall over those 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
