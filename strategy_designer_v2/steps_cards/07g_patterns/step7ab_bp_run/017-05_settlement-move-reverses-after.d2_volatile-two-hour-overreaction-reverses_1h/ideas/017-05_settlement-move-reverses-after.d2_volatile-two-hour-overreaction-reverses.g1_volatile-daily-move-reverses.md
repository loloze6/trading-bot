---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high against its own past month, its 24-hour return is followed by a move the opposite way over the next 24 hours. The larger its 24-hour return against its usual 24-hour move, the larger the move back.
Consequence: A day-long overreaction in a volatile coin can be faded with a move per case several times the cost of a round trip, unlike the 8-hour version.
Why:
- F1: When a coin's 24-hour volatility is at or above its 720-hour average, its next 24 hours run against its prior 24-hour move once that move is at least one usual 24-hour move. Unusual move: +70 bps (t 5.9, 1917 cases) for moves of 1 to 2 usual moves, +61 bps (t 2.5, 687) for 2 to 3, and +149 bps (t 3.1, 328) beyond 3. On the grid shifted by 12 hours the same 1-to-2 bucket gives +46 bps (t 3.4, 1811 cases). Per case this is 2 to 7 times the 0.19 % cost of a buy and a sell.
- F2: In low volatility the same 24-hour reversal is absent or reversed. For 1 to 2 usual moves it is +13 bps (t 0.9, 1202 cases) on one grid and −35 bps (t −2.6, 1135) on the shifted grid, so the reversal belongs to the high-volatility regime.
- F3: The 24-hour reversal after a 24-hour move of at least one usual move shows up separately in each of the 6 coins on the window-start grid, from +25 bps (BTC, t 1.9) to +83 bps (ZEC, t 3.0). It holds in both halves of the windows: +65 bps (t 6.3, 2049 cases) in the early half and +50 bps (t 3.5, 2152) in the late half.
- F7: Over 72 hours there is no reversal of a 72-hour move; if anything it continues. Moves beyond 2 usual moves give −113 bps (t −1.8, 350 cases), so the reversal is a 1-day effect.
