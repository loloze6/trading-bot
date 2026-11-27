---
line: 7.d confirmed, not profitable
backtest: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade_1d
idea tested: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6173 USD
---
## Findings
- **F1:** The Calmar fails because of the short side. In folds B and C the book's deepest fall is −4.44 %, from a peak in w15 to a trough in w16 72 days later. In w16 the short positions on ZEC lost 0.157 (worst bar −0.132), and earlier XRP shorts lost 0.103 in w14 and BTC shorts lost 0.109 in w12. Of the 20 worst position-bars, 75 % are shorts; together they lose 1.02 against a total gain of 2.18.
- **F2:** Rebuilt with a fee of 0.11 % per unit of allocation changed (my approximation, not the engine's exact fees), the long side alone has Calmar 3.36 (yearly +4.1 %, deepest fall −1.2 %, Sharpe 1.63). The short side alone has Calmar 0.44 (yearly +2.8 %, deepest fall −6.3 %, Sharpe 0.53). Both sides together have Calmar 1.53 (deepest fall −4.5 %).
- **F3:** The long fade is the reliable side. Next-day return in the position's direction:
- **F4:** The long side pays only on wide days. In the widest third of range in 30-day swings it earns +3.18 % (t 2.13, 32 cases); the narrow third earns −0.05 % and the middle third −0.10 %. The worst 20 losses sit on days 2.50 swings wide, against 1.55 on average, so width is what enlarges both the gain and the fall.
- **F5:** Longs are stronger after a five-day fall. Inside the profile, drift-adjusted next-day returns of long positions are:
- **F6:** The trade's size covers its cost. The total and unusual move per case is +0.54 %, 2.4 times the 0.22 % cost of a trade. Long positions earn +1.44 % per bar, about 6.5 times the cost. The book is in a position on only 8 % of coin-days, and its daily standard deviation is 0.26 %, so the problem is the depth of the falls, not the cost.

## Ideas
- `077-03.g1.b1.d1.d1_choppy-agitated-low-close-rebound` (from F1, F2, F3, F4, F6): In a choppy, agitated market, a day closing near its low rises over the next day, and the rise is larger the wider the day's range against the coin's 30-day swing of daily returns and the closer the close sits to the low.
- `077-03.g1.b1.d1.d2_low-close-rebound-after-fall` (from F3, F4, F5): In a choppy, agitated market, a day closing near its low after the coin's 5-day return has been falling rises over the next day, more the wider the day's range against the coin's 30-day swing of daily returns and the larger the 5-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
