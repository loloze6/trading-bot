---
line: 7.d confirmed, not profitable
backtest: 067-01.b1.g1.b1.g1_deep-month-slide-accelerates_1d
idea tested: 067-01.b1.g1.b1.g1_deep-month-slide-accelerates
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4758 USD
---
## Findings
- **F1:** The book fails on drift, not on the effect or on fees. It earns +0.87 in summed position-bar gains, of which -2.10 comes from shorting coins whose normal drift is up and about +2.97 from timing; estimated fees are only 0.17. Per case, the total move is +0.33 % against a 1.49 % adverse drift, so only cases far larger than the average short can pay against holding (Sharpe minus holding's -0.58, mean daily return on days in a position 5.5e-05).
- **F2:** The continuation is concentrated in the deepest monthly slides. On the 10-day grid of the choppy profile, the deepest fifth of 30-day returns is followed by a 12.8 % continuation against drift (t 5.79, 32 cases), the next fifth by 4.4 % (t 1.90, 31 cases), and the middle fifth by -4.0 % (t -1.30). Among bet bars, the shallowest forecast tercile loses (-1.2 % unusual, -3.4 % total, 36 cases) while the deep and mid terciles earn +6.1 % and +5.3 %.
- **F3:** The cubic sizing still trades the weak cases. Bet bars where the book was not short show -1.4 % unusual and -3.8 % total (28 cases); bars where it was short show +5.1 % unusual and +2.6 % total (t 2.61, 78 cases).
- **F4:** The book keeps shorts open after the month has turned up, and loses there. Position bars in the profile with a 30-day return at or above 0 (regime "unknown") lose -0.28 % per bar (95 bars). Bars inside the falling-month regime earn +0.085 % (800 bars), and bars carried outside the choppy profile by the 10-bar minimum hold earn +0.044 % (1,020 bars, more than half of all position bars).
- **F5:** The losses sit in short-lived trades and a few windows. Trades of 12 days or less lose -2.0 % to -7.6 % each (272 trades), while trades over 12 days gain +1.8 % (152 trades). Windows w10, w11 and w13 lose -27 %, -31 % and -22 % per trade, in w11 against a holding mean of +1.9 % a day. This is why the book fails with one window left out (-0.099).
- **F6:** Among down-month cases, the continuation is +10.9 % (t 5.25, 41 cases) when the last 10 days swung more than the last 30, against -0.2 % (42 cases) otherwise. It is +10.3 % (t 2.92, 26 cases) when the 60-day return is also negative, against +3.0 % (57 cases) when it is positive. Neither condition was measured alone, without a down month, so neither is used as a repair.

## Ideas
- `067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue` (from F1, F2, F3): In a choppy market, a coin's fall over the past 30 days is followed by a further fall over the next 10 days, only for slides that are deep against the coin's own usual monthly move; the further fall grows with that depth, so the deepest slides carry a move many times their usual size while ordinary slides carry none.
- `067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative` (from F4, F5): In a choppy market, a coin's fall over the past 30 days is followed by a further fall over the next 10 days, only while its 30-day return is still negative; the deeper the remaining monthly fall, the larger the further fall, and the continuation ends once the month's return turns up.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
