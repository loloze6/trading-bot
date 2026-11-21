---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour fall is followed by a rise over the next 24 hours, and the deeper the fall against its usual 24-hour move, the larger the rise.
Consequence: Buying after a sharp one-day fall captures the strongest side of the daily reversal, which a trader can take without shorting.
Why:
- F4: The reversal is stronger after falls than after rises. After a 24-hour fall of at least one usual move the next 24 hours rise +82 bps more than usual (t 6.0, 2011 cases); after a rise they fall +34 bps more than usual (t 3.0, 2190). On the shifted grid the figures are +43 bps (t 3.0) after falls and −9 bps (t −0.7) after rises.
- F1: When a coin's 24-hour volatility is at or above its 720-hour average, its next 24 hours run against its prior 24-hour move once that move is at least one usual 24-hour move. Unusual move: +70 bps (t 5.9, 1917 cases) for moves of 1 to 2 usual moves, +61 bps (t 2.5, 687) for 2 to 3, and +149 bps (t 3.1, 328) beyond 3. On the grid shifted by 12 hours the same 1-to-2 bucket gives +46 bps (t 3.4, 1811 cases). Per case this is 2 to 7 times the 0.19 % cost of a buy and a sell.
- F3: The 24-hour reversal after a 24-hour move of at least one usual move shows up separately in each of the 6 coins on the window-start grid, from +25 bps (BTC, t 1.9) to +83 bps (ZEC, t 3.0). It holds in both halves of the windows: +65 bps (t 6.3, 2049 cases) in the early half and +50 bps (t 3.5, 2152) in the late half.
