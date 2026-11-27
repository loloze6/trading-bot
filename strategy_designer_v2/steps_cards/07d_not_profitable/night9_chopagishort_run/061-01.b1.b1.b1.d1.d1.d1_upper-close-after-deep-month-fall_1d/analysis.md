---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4848 USD
---
## Findings
- **F1:** The tested situation is very rare, which is why trades per day fails. The detector's regime holds on 0.80 % of bars, and in folds B and C it gives only 15 non-overlapping 5-day cases (unusual move +17.7 %, t 3.94). The book is in a position on 2.7 % of bars, over 88 trades. The broader case of the same choppy-market fall has more than twice the cases: the 60-day return within ±10 % and the 20-day return at -10 % or lower, without the upper-close and negative-5-day conditions (agitation not recomputable here). It gives 35 cases, unusual 5-day move +9.40 %, t 3.93, strength 0.73.
- **F2:** The choppy condition is part of the idea's theory and is not an effect of its own. Choppy bars alone give 152 cases at +1.57 % (t 1.53), which leaves about -0.8 % on the 117 choppy cases without a deep 20-day fall. A deep 20-day fall in any trend gives only +1.55 % (515 cases, t 2.85). The same signal in a falling market (60-day return below -10 %) loses: 79 cases at -2.92 % (t -1.89).
- **F3:** The book's gain rests on one window, and its falls come from short squeezes. Window w16 earned +0.170 in summed daily returns, while the whole chain ends at only 1.159. Without w16 the trades sum to about -33 %. In w11 the book lost -0.039 over 7 trades averaging -23.4 %, and the worst trade lost -62.8 %. The book's deepest fall is -4.7 % against a yearly return of +2.1 % (Calmar 0.36). All 10 of its worst days came on days when the coins rose, between +1.9 % and +22.7 % (worst: -4.0 % on a +18.4 % day).
- **F4:** The grade "deeper 20-day fall, larger short" fails beyond about -20 %. Among upper-half closes after a negative 5-day return, the unusual 5-day move is:
- **F5:** The move keeps growing after five days, and the cost is small against it. Over 10 days the broad choppy deep-fall case gives +15.6 % (20 cases) against +9.4 % over 5 days, and the regime's own cases give +16.2 % (11 cases). A trade costs 0.22 %, 13 times less than the tested total move per case. So the failure lies in rarity, in one window and in squeeze days, not in fees.

## Ideas
- `061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues` (from F1, F2, F4): In a choppy market, a coin whose 20-day return is a deep fall falls further over the next five days, and the deeper that 20-day fall is, the larger the further fall, up to falls of about a fifth of its price.
- `061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day` (from F3, F5, F1): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, while its 20-day return is a deep fall, its price falls over the next ten days, and the deeper that 20-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades` (from F4, F3, F2): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, while its 20-day return is a fall of a tenth to a fifth of its price, its price falls over the next five days, and the nearer that close is to the day's high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
