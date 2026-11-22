---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day hourly volatility is low against its own last 6 months, its move from Wednesday 00:00 to Friday 00:00 UTC continues in the same direction over Friday and Saturday. The larger that move, the larger the continuation.
Consequence: In calm weeks a trader would follow the mid-week direction into the end of the week rather than fade it.
Why:
- F4: In calm volatility (ratio ≤ 1), the 48-hour move from Wednesday 00:00 to Friday 00:00 continues over Friday and Saturday: slope +0.161 (t 4.73, 595 cases), sign-weighted move +0.096 usual moves (t 2.97). The same 48-hour test on Mondays in calm gives slope +0.076 (t 1.07, 627 cases). This is the strongest of the 14 weekday × volatility cells.
- F5: The tested Monday continuation is not graded by the weekend move's size. By size tercile of the weekend move, the sign-weighted move is +0.095 (t 2.83) for the smallest, +0.058 (t 1.65) for the middle and −0.035 (t −0.78) for the largest. It shows in the low-volatility tercile only (slope +0.172, t 2.04), against −0.082 and −0.017 in the mid and high terciles.
