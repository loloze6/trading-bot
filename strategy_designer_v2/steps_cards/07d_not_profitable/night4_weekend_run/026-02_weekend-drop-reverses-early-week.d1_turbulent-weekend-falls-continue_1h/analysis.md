---
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3752 USD
---
## Findings
- **F1:** The book earns almost nothing against simply holding the coins. Its mean daily return is 5.2e-05 against about 0.0007–0.0016 for holding each coin, for example BTC 0.00118 and ZEC 0.00155. Its Sharpe is 0.20 against holding's 0.55. In the rising windows it lags far behind holding: w11 book −0.00082 a day against holding +0.01256, and w16 −0.00067 against +0.00454.
- **F2:** The forecast's grading does not work. Across the five |forecast| quintiles of the 804 short cases, the short excess move runs +0.58 %, +0.53 %, −0.06 %, +0.05 %, +0.44 %, with no rise from bottom to top. Meanwhile the position grows from −0.02 to −0.76 of the book (correlation of forecast with allocation 0.87). The plan's own check of upper minus lower half was −0.00106.
- **F3:** The size of the weekend fall points the wrong way, so scaling by it puts the largest bets on the cases that reverse.
- **F4:** The weekend's volatility against the prior week is what carries the continuation.
- **F5:** The same turbulence effect appears after weekend rises.
- **F6:** The result rests on a few windows.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.d1_turbulence-not-fall-size` (from F2, F3, F4): When a coin falls over the weekend (Saturday 00:00 to Monday 00:00 UTC), it keeps falling over Monday and Tuesday. The fall grows with how much more volatile the weekend's hours were than the coin's previous week, not with how far the coin fell over the weekend.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.d2_turbulent-weekends-continue-both-ways` (from F1, F4, F5, F6): Over Monday and Tuesday, a coin keeps moving in its weekend's direction (Saturday 00:00 to Monday 00:00 UTC). The more volatile the weekend's hours were compared with the coin's previous week, the larger that continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
