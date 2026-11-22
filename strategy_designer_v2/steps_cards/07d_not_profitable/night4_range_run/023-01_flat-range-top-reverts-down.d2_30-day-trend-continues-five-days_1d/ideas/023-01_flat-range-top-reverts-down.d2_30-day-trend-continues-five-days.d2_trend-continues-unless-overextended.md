---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days, and the smaller its 90-day return in that same direction, the larger that continuation.
Consequence: A trader would follow a 30-day trend that starts from a flat or opposite 90-day move and refuse one that extends an already long run.
Why:
- F1: The Calmar fails (0.29) because the chained book falls 63 % from its peak against a yearly return of 18 %, and that fall builds through windows w3 to w10: w3, w4, w5, w7, w8 and w9 all lose (-23.5 %, -10.8 %, -17.9 %, -9.5 %, -5.4 %, -4.8 %), and the trough comes in w10.
- F2: Inside w3–w10 the short side carries the loss: shorts sum -2.35 (mean -0.00131 per bar, 1795 bars) and longs only +0.33. Outside that stretch shorts sum +2.02 and longs +12.10, and over all windows shorts make nothing (mean -0.00006 over 5173 bars against +0.00232 for longs).
- F4: The book loses when the 30-day move it follows is already extreme. Positions whose 30-day return in their direction is above 35 % earn -0.00066 per bar (t -0.73, 2039 bars), against +0.00251 (t 2.9) for 22–35 %. Shorts after a 30-day fall of more than 35 % lose -2.50 in sum (mean -0.00384, 652 bars).
- F5: A long run behind the position also predicts losses. Positions whose 90-day return in their direction is above 27 % earn -0.00036 and -0.00009 per bar, against +0.00151 (t 1.9) and +0.00148 when the 90-day move is against or flat. Inside w3–w10, a 90-day move above 52 % in the position's direction earns -0.00196 per bar, while a flat 90-day move earns +0.00383.
