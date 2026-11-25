---
line: 7.d confirmed, not profitable
backtest: 039-01_agitated-swing-fall-low-close-rebound_1d
idea tested: 039-01_agitated-swing-fall-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3600 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.68 against 0.75). On folds B and C the book's chained daily returns make +21.9 % a year with a deepest fall of −25.7 %. That fall is one 19-day episode inside w16, where the book lost a summed −27.1 % while its coins' summed daily returns were −69.5 %. Every other window's deepest fall is at or under −11.0 %, except w13 at −22.2 %.
- **F2:** The effect lives only in a falling 60-day trend. On agitated bars, the next-day return minus the coin's mean is:
- **F3:** Being in a falling market is not an effect of its own. Agitated falling bars without the signal are followed by −1.05 % (t −3.94, 361 cases), against +1.40 % with it. The falling trend is the setting of the brief's own theory, where leverage is being cut and forced sellers overshoot.
- **F4:** Inside the falling agitated profile the effect stays graded. Splitting the signal bars into thirds by forecast, the next-day excess return rises from +0.38 % (134 cases) to +1.36 % (147) to +2.89 % (96). In rising markets the thirds give −0.35 %, +0.66 % and −0.16 %, with no grading.
- **F5:** The w16 deepest fall was carried by positions taken in rising markets, while positions taken in falling markets mostly earned. On w16's held bars by 30-day trend:
- **F6:** A deeper fall over the prior days strengthens the same situation without being an effect alone. On agitated bars in the quarter with the largest 3-day fall (mean −15.7 % on held bars):

## Ideas
- `039-01.d1_falling-agitated-forced-selling-rebound` (from F1, F2, F3, F4, F5): In a falling, agitated market, the larger a one-day fall against the coin's 30-day standard deviation of daily returns, and the nearer that day's close sits to its low within the day's range, the larger the rise over the next day; the rise grows with the two together.
- `039-01.d2_multi-day-slide-low-close-rebound` (from F1, F5, F6): In an agitated market, the larger a one-day fall against the coin's 30-day standard deviation of daily returns, the nearer that day's close sits to its low, and the larger the coin's fall over the last 3 days, the larger the rise over the next day; the rise grows with the three together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
