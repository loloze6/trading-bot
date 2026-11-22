---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell over that stretch, the wider that stretch's range against its 30-day average, the higher the coin's return over the next 7 days, whatever the coin's 90-day return.
Consequence: A trader holds panic purchases for a week instead of two, which keeps most of the premium and frees capital to take the next panic sooner.
Why:
- F1: Both failing measures come from how rarely the book is in the market: it holds a position on 7.7 % of 17,525 coin-days and makes 172 trades, so trades per day are 0.0094 (the rule is 0.01) and the mean daily return is 0.000465 (the rule is 0.0005), although it earns 0.594 % on each day it is in, and only 0.000086 of that daily mean comes from the market's own rise.
- F3: Panics in any trend carry the premium: on the first bar per 84-bar cell with range ratio ≥ 2 and a 24h fall, the unusual 14-day return is +3.01 % (t 2.36, 291 cases, strength 0.143); at ratio ≥ 2.5 it is +4.24 % (t 2.69, 169 cases, strength 0.195); and over 7 days it is +3.90 % (t 3.21, 176 cases, strength 0.176).
- F6: The width of the range against its 30-day average does grade the rebound, at least up to about 3 times: by grid-cell maximum ratio the unusual 14-day returns are −1.84 % (t −2.02) at 1.5–2, +0.67 % at 2–2.5, +2.89 % (t 1.59) at 2.5–3, and +1.66 % above 3.
- F8: The trend over the 14 days before the panic does not decide the rebound, as the brief says: by prior-14-day-return quartile the unusual 14-day returns are +4.04 %, +0.84 %, +5.37 % (t 2.27) and +1.82 %.
