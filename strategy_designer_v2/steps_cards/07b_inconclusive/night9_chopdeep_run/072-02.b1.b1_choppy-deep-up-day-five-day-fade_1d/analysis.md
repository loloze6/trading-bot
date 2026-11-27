---
line: 7.b inconclusive
backtest: 072-02.b1.b1_choppy-deep-up-day-five-day-fade_1d
idea tested: 072-02.b1.b1_choppy-deep-up-day-five-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4131 USD
---
## Findings
- **F1:** The effect sits in the deepest closes only. In folds B and C, on choppy up days, the deepest fifth of depth had a 5-day unusual move of -7.27 % (winsorised, 26 cases), against +0.21 % for the other four fifths (Welch t -2.82). The four shallower fifths gave -2.4 %, -1.2 %, -0.2 % and +9.2 %, with no steady gradient between them. A linear slope on the whole forecast therefore dilutes the effect, and step 5's slope t is only 0.94, on 841 cases.
- **F2:** The same shape shows the next day. On choppy up days, the deepest fifth fell -1.48 % beyond drift over one day (t -3.42, 153 cases), against -0.24 % for the rest (Welch t -2.72). The linear slope at 1 day has t 1.49 only, on 1,029 cases.
- **F3:** The linear slope is pulled about by single extreme moves in the shallow fifths. One DOGE case in w11, in the shallowest fifth, rose +384 % over 5 days, and that fifth's standard deviation is 0.53 against about 0.06 to 0.13 elsewhere. Winsorising at 1 % and 99 % moves the 5-day up-day slope t in folds B and C from 2.14 to 2.41, and the rank correlation is 0.17 (p 0.02, 184 cases).
- **F4:** The deep-close fall is not confined to a few periods. The deepest fifth's 5-day unusual move is negative in 9 of 12 windows (w7 to w18), with the largest in w16 (-30 %, 6 cases), and it holds on down days too (-5.5 % against -1.5 %, Welch t -1.82). The effect is the depth, read in its strongest cases, as the brief claims.
- **F5:** The idea's size is real but small against the market's drift. The unusual move is +0.78 % per case over 5 days (t 2.18, 936 days, strength 0.068), which is 3.5 times the 0.22 % cost of a trade. But the coins' normal drift is -0.80 % in the short direction, so the total move per case is -0.03 %, and the book's Sharpe is -0.03.

## Ideas
- `072-02.b1.b1.b1_deepest-up-day-five-day-fade` (from F1, F3, F4): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next five days. The fall grows faster than the depth, so the closes deepest below the high carry most of it.
- `072-02.b1.b1.b2_deepest-up-day-next-day-fade` (from F2, F3): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day. The fall grows faster than the depth, so the closes deepest below the high carry most of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
