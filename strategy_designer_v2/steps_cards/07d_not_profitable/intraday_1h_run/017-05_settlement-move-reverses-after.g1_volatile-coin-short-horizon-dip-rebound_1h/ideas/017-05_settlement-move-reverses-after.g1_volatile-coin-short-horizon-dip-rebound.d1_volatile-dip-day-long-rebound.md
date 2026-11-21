---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's recent hourly volatility (its 7-day mean absolute hourly move) is high, the larger its 2-hour fall relative to its usual 2-hour move, the larger its rise over the next 24 hours, at any hour of the day, with the rise larger the higher that 7-day volatility ranks against the coin's own last 30 days.
Consequence: A sharp 2-hour fall in a volatile coin is a reason to hold a rebound position for a day rather than two hours, so the expected move is several times the round-trip fee and the position is turned over far less.
Why:
- F1: Before fees the book earns money on every coin, with summed bar gains of 2.49 to 4.78 (20.95 over the six coins), but fees cost 5.96 to 7.98 per coin (40.60 in total), so every coin loses after fees (net -1.91 to -5.25); fees run at 0.10% of each unit traded over about 40,000 units of turnover.
- F2: Turnover comes from trading in and out of a 2-hour signal: 27,119 opens, 27,128 closes and 41,322 resizes (14,915 units, the largest share of the fees, 16.07); the closes alone cost 12.24 on bars held flat.
- F4: The rebound is too small at 2 hours for most signals. The 2-hour excess return is only 2.1 bp in the lowest positive-forecast quintile and 4.4–6.6 bp in the middle ones, against about 20 bp of fees for a round trip; only the top quintile reaches 21 bp.
- F5: The rebound keeps building past 2 hours. The top quintile's excess return grows from 21 bp at 2 hours to 25 bp at 8 hours and 73 bp at 24 hours, and the second quintile's from 6.6 bp to 14.0 bp at 24 hours.
- F6: The rebound is graded by the coin's volatility rank, not switched on by it:
- F7: At 24 hours the volatility grading is starker. Falls of 2–3 usual moves are followed by -41 bp in the lowest vol-rank quarter, +31 bp at rank 0.5–0.75 and +164/+137 bp in the top two vol-rank groups. Falls beyond 3 usual moves follow the same pattern: -65 bp, then +56 bp, then +253/+249 bp.
