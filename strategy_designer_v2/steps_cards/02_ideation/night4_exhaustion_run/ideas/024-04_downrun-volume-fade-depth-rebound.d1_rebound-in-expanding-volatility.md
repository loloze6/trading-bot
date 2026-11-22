---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound
line: 7.d not profitable
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while the coin's 7-day volatility is high relative to its 30-day volatility. The higher that ratio, the larger the rise.
Consequence: A trader would buy down-streaks that come in an agitated, volatility-expanding market, and would stay out of quiet-market streaks, which keep falling.
Why:
- F2: The failing Calmar of 0.35 comes from one long fall of −76 % in the chained book, running from w12 to w16 over 485 days. In those windows the coin's next-bar return averaged only 0.000048 against 0.000269 elsewhere. The coin's 30-day return was negative on 45 % of bars against 35 % elsewhere. The book stayed about 0.82 long and lost 0.000032 per bar.
- F3: The idea's own effect is far below what a trade costs. The unusual move is +0.06 % per case over 3 days (strength 0.008, t 0.54, 5713 cases), or 0.3 times the 0.19 % cost of a trade. The volume-fade split went the wrong way: above-median fade minus below-median was −0.58 %. Nearly all the book's gain is the coin's drift of +0.41 % per 3 days.
- F4: Down-streak cases rebound only when the coin's recent volatility is high against its 30-day level. In the top quarter of 7-day over 30-day volatility (mean ratio 1.35), the 3-day excess return is +1.69 % (t 3.99, 533 cases). In the bottom quarter (ratio 0.61) it is −0.73 % (t −2.32, 534 cases). On long bars, the top fifth of this ratio carries 16.1 of the book's 19.1 summed bar gain.
