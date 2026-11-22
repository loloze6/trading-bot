---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell over that stretch, the wider that stretch's range against its 30-day average, the higher the coin's return over the next 14 days, whatever the coin's 90-day return.
Consequence: A trader buys panics in coins inside a longer decline too, and sizes the bet by how far the 24-hour range exceeds its usual size rather than by the 90-day rise, which more than triples the number of trades.
Why:
- F1: Both failing measures come from how rarely the book is in the market: it holds a position on 7.7 % of 17,525 coin-days and makes 172 trades, so trades per day are 0.0094 (the rule is 0.01) and the mean daily return is 0.000465 (the rule is 0.0005), although it earns 0.594 % on each day it is in, and only 0.000086 of that daily mean comes from the market's own rise.
- F2: The 90-day-rise condition is what makes the signal rare: of 206 grid cells whose 24h range reached at least 2 times its 30-day average with a 24h fall, only 24 had a positive 90-day return, and at 3 times only 7 of 76 did.
- F3: Panics in any trend carry the premium: on the first bar per 84-bar cell with range ratio ≥ 2 and a 24h fall, the unusual 14-day return is +3.01 % (t 2.36, 291 cases, strength 0.143); at ratio ≥ 2.5 it is +4.24 % (t 2.69, 169 cases, strength 0.195); and over 7 days it is +3.90 % (t 3.21, 176 cases, strength 0.176).
- F4: The size of the 90-day rise does not grade the rebound: across 90-day-return quartiles of the ratio-≥2 cases, the unusual 14-day returns are +0.47 %, +1.79 %, +0.46 % and +3.54 % (about 17 cases each, no t above 1.4); in round 1, cases with the 90-day return up earned +0.75 % (24 cases) against +1.20 % with it down (182 cases).
- F6: The width of the range against its 30-day average does grade the rebound, at least up to about 3 times: by grid-cell maximum ratio the unusual 14-day returns are −1.84 % (t −2.02) at 1.5–2, +0.67 % at 2–2.5, +2.89 % (t 1.59) at 2.5–3, and +1.66 % above 3.
- F7: Costs are not the cause: the total move per case is +6.78 % against a cost of 0.19 % per trade, and the 172 trades net a mean of +11.1 % (median +1.66 %, 60 % winners).
