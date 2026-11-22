---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days, only while that move is young: the fewer days since the 30-day net move became large relative to the range, the larger the continuation.
Consequence: A trader would follow a fresh 30-day trend over the next 5 days and give less weight to one that has already been in place for more than about a week.
Why:
- F1: The Calmar fails (0.29) because the chained book falls 63 % from its peak against a yearly return of 18 %, and that fall builds through windows w3 to w10: w3, w4, w5, w7, w8 and w9 all lose (-23.5 %, -10.8 %, -17.9 %, -9.5 %, -5.4 %, -4.8 %), and the trough comes in w10.
- F3: The gain sits in the first days after the trending regime starts and fades as the regime ages. Days 1–2 earn 0.00191 per bar (t 4.0, 3938 bars), days 3–4 earn 0.00122 (t 1.5), days 5–9 earn 0.00103 (t 1.1) and beyond day 9 earn 0.00002 (t 0.03). In w3–w10 only days 1–2 gain (+0.86); every later group loses (-1.11, -0.97, -0.81).
