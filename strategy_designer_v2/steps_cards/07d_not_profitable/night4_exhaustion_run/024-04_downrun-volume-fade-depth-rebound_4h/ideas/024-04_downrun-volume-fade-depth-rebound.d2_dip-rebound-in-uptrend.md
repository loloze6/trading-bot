---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound
line: 7.d not profitable
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while the coin's 30-day return is positive. The larger the streak's loss in usual moves, the larger the rise.
Consequence: A trader would buy deep pullbacks inside a rising month and refuse them inside a falling month, which removes the exposure that produced the deepest fall.
Why:
- F1: The book is a near-copy of holding the coins, so it carries their falls. It held a long position on 99.4 % of bars, and its mean allocation was 1.015 even on bars where the forecast was 0 (51 % of bars). Its daily returns correlate 0.917 with the coins' daily returns, with a beta of 0.857. Its window sums track holding's (w14 −0.76 against −0.52; w2 −0.48 against −0.46).
- F2: The failing Calmar of 0.35 comes from one long fall of −76 % in the chained book, running from w12 to w16 over 485 days. In those windows the coin's next-bar return averaged only 0.000048 against 0.000269 elsewhere. The coin's 30-day return was negative on 45 % of bars against 35 % elsewhere. The book stayed about 0.82 long and lost 0.000032 per bar.
- F5: The rebound after a deep streak shows inside a rising month and fails inside a falling one. With a positive 30-day return, the deepest quarter of streak losses gives +2.11 % excess over 3 days (t 3.30, 238 cases). With a non-positive 30-day return, the shallowest quarter gives −1.28 % (t −2.40, 276 cases). Cases with a 30-day return between −19 % and −6 % give −1.20 % (t −3.23, 426 cases). That last band is the state that dominated the w12–w16 fall.
