---
line: 7.d confirmed, not profitable
backtest: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade_1d
idea tested: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4492 USD
---
## Findings
- **F1:** The failing measures (Calmar 0.31, Sharpe below holding's) come from cases where the bounce has already recovered the coin's past week. Cases whose 5-day return, including the up day, is still negative are followed by a next-day short excess of +2.79 % (t 4.82, n 120, hit 71 %). Cases whose 5-day return is at or above 0 give +0.12 % (t 0.41, n 253). That is well under the 0.22 % cost of a trade.
- **F2:** Keeping only those still-down cases, with fees approximated, lifts the book's Sharpe from 0.59 to 1.37. Its deepest fall shrinks from -9.5 % to -2.4 %. Its Calmar rises from 0.40 to 2.27. This changes both failing measures.
- **F3:** The condition is not an effect of its own. On falling-market days with a negative 5-day return but no signal, the next-day short excess is +0.32 % (t 2.36, n 1504). The same days with the signal give +2.90 % (t 5.18, n 75). Signal days with a 5-day return at or above 0 give +0.28 % (t 0.65, n 156). The condition fits the brief's theory: a relief bounce that has not yet undone the recent fall is short-covering that gets given back, not a turn.
- **F4:** The effect grows with how far the coin is still down over 5 days. By quintile of the 5-day return, the short excess is +3.36 % (t 3.78), then +1.34 % (t 2.79), then -0.04 %, then -0.57 % from the lowest to the fourth quintile; the highest quintile gives +1.15 % (t 1.78).
- **F5:** The book's falls come from rebounds that kept going. Its 10 worst days fell on days when the coins rose +1 % to +15 %. The deepest fall (40 days, -9.4 %) sits in w13, where cases earned only +0.32 % (t 0.33, n 51) and only 35 % had a negative 5-day return. Among the 15 worst cases, only 33 % had a negative 5-day return; their mean 5-day return was +6.1 %.
- **F6:** The still-down cases pay in every year seen:
- **F7:** In an agitated market (30-day swing above the 90-day swing, a proxy for the profile's agitation), cases give +2.04 % (t 3.40, n 72) against +0.73 % (t 2.30, n 301) when calm. The same agitated falling days without the signal give -0.20 % (t -1.00, n 841), so agitation is not the effect by itself.
- **F8:** The idea's own grading by width does not hold. By width quartile, the excess is +1.32 %, +1.23 %, +0.23 % and +1.60 %. Among the still-down cases, the narrowest tercile earns the most (+4.32 %, t 3.94).

## Ideas
- `074-01.b1.b1.b1.b1.d1_still-down-wide-bounce-fade` (from F1, F2, F3, F4, F5, F6): In a falling market, an up day whose high-to-low range is wide against the coin's average daily range over the past 20 days and that closes near its high, while the coin's 5-day return including that day is still negative, is followed by a fall over the next day. The more the coin is still down over those 5 days, the larger the next day's fall.
- `074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade` (from F7, F3): In a falling, agitated market, an up day whose high-to-low range is wide against the coin's average daily range over the past 20 days and that closes near its high is followed by a fall over the next day. The wider that day's range and the nearer its close to the high, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
