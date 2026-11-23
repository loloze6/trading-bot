---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, multiplied by the coin's 2-day volatility against its usual 30-day level, the larger the rise.
Consequence: A trader sizes the settlement-fall rebound up rather than down when the coin is agitated, and passes on small falls in calm markets whose rebound does not cover the fee.
Why:
- F2: Most cases are too small to pay: at the 16:00 close the 8-hour return after a fall is +0.086 % (t 1.1, n 1153) for forecasts up to 2 and +0.089 % (t 1.3, n 1607) for forecasts 2 to 5, both below the 0.19 % cost; it is +0.42 % (t 6.5, n 2111) for forecasts 10 to 20; and the two smallest fall quintiles give +0.07 % and +0.04 % (t 1.2 and 0.5) against +0.48 % and +0.30 % (t 6.5 and 3.2) for the two largest.
- F3: The rebound after a fall is concentrated where the coin's recent volatility is high: among the two largest fall quintiles, the 8-hour return is +0.85 % (t 6.5, n 1110) in the top tercile of the coin's 48-hour mean absolute 2-hour move against its 720-bar usual, against +0.27 % (t 4.0) in the bottom tercile and +0.05 % (t 0.5) in the middle one.
- F4: High volatility is not an effect of its own: at the 16:00 close in the high-volatility tercile, the 8-hour return is +0.62 % (t 6.0, n 1587) after a large fall and +0.31 % (t 3.2, n 1229) after a small fall, but only +0.07 % (t 1.0, n 2759) after a rise, so the condition alone earns about a tenth of what it earns with the signal; it belongs to the idea's theory, since crowded, expensive positions and forced flows around settlement are largest in agitated markets.
- F6: The book's volatility-target sizing works against the effect: it shrinks the position in exactly the high-volatility states where the move is largest (F3). Its mean position is 0.25 of the book in the 8 hours after 16:00 and 0.37 of the book when it is in a position, so the trade-level gross gain of +0.32 % per trade (13404 long trades, net +0.22 %) does not reach the book, which has a mean daily return of -0.002 % on days in a position.
