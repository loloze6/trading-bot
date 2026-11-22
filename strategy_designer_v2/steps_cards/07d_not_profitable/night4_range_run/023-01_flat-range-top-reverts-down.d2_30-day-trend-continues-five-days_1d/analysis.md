---
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3517 USD
---
## Findings
- **F1:** The Calmar fails (0.29) because the chained book falls 63 % from its peak against a yearly return of 18 %, and that fall builds through windows w3 to w10: w3, w4, w5, w7, w8 and w9 all lose (-23.5 %, -10.8 %, -17.9 %, -9.5 %, -5.4 %, -4.8 %), and the trough comes in w10.
- **F2:** Inside w3–w10 the short side carries the loss: shorts sum -2.35 (mean -0.00131 per bar, 1795 bars) and longs only +0.33. Outside that stretch shorts sum +2.02 and longs +12.10, and over all windows shorts make nothing (mean -0.00006 over 5173 bars against +0.00232 for longs).
- **F3:** The gain sits in the first days after the trending regime starts and fades as the regime ages. Days 1–2 earn 0.00191 per bar (t 4.0, 3938 bars), days 3–4 earn 0.00122 (t 1.5), days 5–9 earn 0.00103 (t 1.1) and beyond day 9 earn 0.00002 (t 0.03). In w3–w10 only days 1–2 gain (+0.86); every later group loses (-1.11, -0.97, -0.81).
- **F4:** The book loses when the 30-day move it follows is already extreme. Positions whose 30-day return in their direction is above 35 % earn -0.00066 per bar (t -0.73, 2039 bars), against +0.00251 (t 2.9) for 22–35 %. Shorts after a 30-day fall of more than 35 % lose -2.50 in sum (mean -0.00384, 652 bars).
- **F5:** A long run behind the position also predicts losses. Positions whose 90-day return in their direction is above 27 % earn -0.00036 and -0.00009 per bar, against +0.00151 (t 1.9) and +0.00148 when the 90-day move is against or flat. Inside w3–w10, a 90-day move above 52 % in the position's direction earns -0.00196 per bar, while a flat 90-day move earns +0.00383.
- **F6:** The book trades enough to cover its cost: the idea's total move is +0.73 % per 5-day case against a cost of 0.19 % per trade, 3.8 times the cost. So the failure lies in when the book holds, not in fees.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d1_young-trend-continues-further` (from F1, F3): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days, only while that move is young: the fewer days since the 30-day net move became large relative to the range, the larger the continuation.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d2_trend-continues-unless-overextended` (from F1, F2, F4, F5): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days, and the smaller its 90-day return in that same direction, the larger that continuation.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d3_extreme-monthly-moves-revert` (from F2, F4): In a coin whose 30-day return has been extreme relative to its 30-day high-low range, the larger that 30-day return, the further the coin moves back against it over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
