---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
idea tested: 017-05_settlement-move-reverses-after
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4707 USD
---
## Findings
- **F1:** The book loses to fees, not to the forecast. Its position earns 1.15 bps a day before costs and pays 27.5 bps a day in fees, so its mean daily return is −0.26 % (Sharpe −6.97) while the coins' own mean daily return is +0.12 %.
- **F2:** The trades are too short to carry the edge. The 43,508 trades last a median 60 minutes and lose 0.098 % gross each (t −18.0). On each settlement bar the one-bar position gains 0.39 bps but pays 4.6 bps of fee, at a mean absolute allocation of 0.43.
- **F3:** The reversal is real but small and slow. On the 51,888 settlement bars the forecast-signed forward return is 1.8 bps over 1 hour (t 3.6), 3.7 bps over 2 hours (t 5.6) and 5.6 bps over 8 hours (t 4.5). The mean absolute pre-settlement 2-hour move is 94 bps, and the slope of the 8-hour return on that move is only −0.086.
- **F4:** The reversal lives almost entirely in high volatility. Split by the coin's 24-hour volatility into thirds, the signed 2-hour return is 0.5 bps in the low third (t 0.76), 2.2 bps in the middle (t 2.3) and 8.4 bps in the high third (t 5.0). Scaled by volatility it also doubles at each step (0.013, 0.026, 0.050).
- **F5:** Inside high volatility the reversal grows with the size of the pre-settlement move. The signed 2-hour return is −4.4 bps for small moves, 5.4 bps for mid moves and 14.1 bps for large moves (t 5.6). The 8-hour return for large moves is 18.8 bps (t 4.2, n 9,520). In low volatility, large moves show −1.7 bps over 2 hours and −4.5 bps over 8 hours.
- **F6:** Across all volatility, the reversal does not grow with forecast size. By |forecast| quintile the signed 1-hour return runs −0.9, 3.6, 1.4, 5.4 and −0.3 bps. A move standardised against its own recent size therefore does not pick out the strong cases that raw volatility does.
- **F7:** A pre-settlement move against the coin's 24-hour trend reverses more over 2 hours: 5.7 bps (t 5.8, n 21,605), against 2.4 bps (t 2.6) when it runs with the trend. In high volatility, though, the moves that run with the trend give back more over 8 hours: 19.3 bps (t 4.7), against 2.5 bps.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-reversal-in-high-volatility` (from F1, F2, F3, F4, F5, F6): The return over the 8 hours after each funding settlement time (00, 08, 16 UTC) runs opposite to the return over the 2 hours before it, and the larger the pre-settlement move, the larger the move back. This holds only while the coin's 24-hour volatility is high, and the reversal is larger the higher that volatility.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses` (from F7, F3): Over the 2 hours after a funding settlement time, a coin gives back more of its 2-hour pre-settlement move the more that move runs against the coin's own 24-hour return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
