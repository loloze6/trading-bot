---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1_high-close-location-fades-weekly_1d
idea tested: 061-01.b1.b1.b1_high-close-location-fades-weekly
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4572 USD
---
## Findings
- **F1:** The book's deepest fall (-8.3 % over 19 days, from w15 into w16) comes from shorts taken after a 5-day rise. The three worst trades are all one w16 entry, with a prior 5-day return of +24 % and a day return of 1.8 times the usual daily swing (-60.6 %, -42.3 % and -33.7 % net). Trades entered after a negative 5-day return made +1.30 % net on average (55 trades, worst -15.8 %). Trades entered after a positive one made -3.69 % (62 trades, worst -60.6 %). This is why Calmar is 0.37 against 0.75, and why the Sharpe is 0.544, 0.008 below holding's.
- **F2:** The prior 5-day fall belongs to the effect and is not an effect of its own. Inside the choppy, agitated profile, a high close after a negative 5-day return was followed by an unusual 5-day short-side move of +5.6 % (t 3.72, 44 cases). The same negative 5-day return without a high close gave +0.6 % (t 0.57, 203 cases). A high close after a positive 5-day return gave +0.7 % (t 0.53, 48 cases). By quartile of the prior 5-day return, the signal's move grades from +6.4 % (lowest quartile) through +4.9 % and +1.8 % to +0.5 % (highest). This fits the theory: a late push to the top of a range that has just fallen is absorbed and given back, while a push extending a 5-day run is a breakout that carries on.
- **F3:** The size of the day's gain grades the effect the same way, and it is not an effect alone either. By quartile of the day's return over its 20-day swing, the signal's unusual 5-day move falls from +6.3 % (t 2.86) through +4.9 % and +3.6 % to -1.3 % (t -0.55, the largest up days). Signals below the top quartile gave +5.0 % (t 4.15, 64 cases), while the same modest-day condition without a high close gave +0.6 % (t 0.77, 294 cases).
- **F4:** The effect builds beyond five days. The signal's unusual short-side move is +0.7 % over 2 days (t 0.70), +3.1 % over 5 days (t 2.92, 92 cases) and +4.9 % over 10 days (t 3.31, 89 cases). Trades held 6 to 8 days averaged +6.0 % net (8 trades), against +2.6 % for those held 5 days (53 trades).
- **F5:** Early exits lose, and a move against the short does not end the fall. Trades closed within 4 days, before a window's end, averaged -7.1 % net (42 trades, exit forecast about -1.1, against -17.0 at entry). Trades held at least 5 days averaged +1.9 % (71 trades). When the coin rose over the first 2 days, the short still gained +2.8 % over the remaining 3 days (44 cases), against +0.8 % when it had fallen (48 cases).
- **F6:** The edge does not hold the same way across windows or across the closest closes in folds B, C. w12 lost (unusual move -4.0 %, t -2.20, 16 cases) and w17 was flat (+0.2 %, 14 cases), while w18 gave +8.1 % (t 4.15, 20 cases). By close location, the signal's move was +3.6 % (0.8 to 0.9), +1.1 % (0.9 to 0.97) and +4.8 % (0.97 and above), not a monotone grade.

## Ideas
- `061-01.b1.b1.b1.d1_high-close-after-fall-fades` (from F1, F2, F6): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the deeper that 5-day fall and the nearer the close is to the day's high, the larger the fall.
- `061-01.b1.b1.b1.d2_quiet-high-close-fades` (from F1, F3): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range on a day whose gain is small against its usual daily swing, its price falls over the next five days, and the smaller the day's gain against that swing, the larger the fall.
- `061-01.b1.b1.b1.d3_high-close-fades-over-ten-days` (from F4, F5): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range, its price falls over the next ten days, and the nearer the close is to the day's high, the larger the fall, including after the price has first risen for two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
