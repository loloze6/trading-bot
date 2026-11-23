---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, while the coin's 2-day volatility is raised against its usual 30-day level, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader takes the settlement-fall rebound only in agitated markets, held for a day, so that one trade captures a move several times its cost instead of paying fees on small rebounds.
Why:
- F1: The book's gain is eaten by its fees: over all bars it earns 0.183 bp per bar before costs and pays 0.178 bp per bar in fees, with the fees landing on the entry bar (2.12 bp at the 16:00 close) and the exit bar (2.05 bp eight hours later), so a Sharpe of -0.02 and a yearly return of -2.0 % follow from a move per case (+0.23 % total) only 1.2 times the 0.19 % cost of a trade.
- F3: The rebound after a fall is concentrated where the coin's recent volatility is high: among the two largest fall quintiles, the 8-hour return is +0.85 % (t 6.5, n 1110) in the top tercile of the coin's 48-hour mean absolute 2-hour move against its 720-bar usual, against +0.27 % (t 4.0) in the bottom tercile and +0.05 % (t 0.5) in the middle one.
- F4: High volatility is not an effect of its own: at the 16:00 close in the high-volatility tercile, the 8-hour return is +0.62 % (t 6.0, n 1587) after a large fall and +0.31 % (t 3.2, n 1229) after a small fall, but only +0.07 % (t 1.0, n 2759) after a rise, so the condition alone earns about a tenth of what it earns with the signal; it belongs to the idea's theory, since crowded, expensive positions and forced flows around settlement are largest in agitated markets.
- F5: In the high-volatility tercile the large-fall rebound keeps building past 8 hours, to +0.82 % over 24 hours (t 5.0, n 1577), 4.3 times the cost of a trade, against +0.06 % and +0.09 % over 24 hours in the low and middle terciles (t 0.4 and 0.6) and +0.11 % (t 1.1) after rises in high volatility.
