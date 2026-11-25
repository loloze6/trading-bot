---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.b1_one-day-rise-fades-wider_1d
idea tested: 058-01.g2.b1_one-day-rise-fades-wider
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4533 USD
---
## Findings
- **F1:** The book loses after the signal bar, not on it: in the 690 bars where a fresh short signal was held, the position gained +0.17 % per bar (sum +1.15); in the 487 bars it was carried after the signal it lost -0.21 % per bar (sum -1.02); trades lasting 3–5 days lost -2.86 % net (79 trades) and 5–10 days lost -3.27 % (128 trades), against -1.19 % for trades of 3 days or less (366); all 617 trades were short, -1.65 % gross and -1.75 % net on average, giving a Sharpe of -0.03.
- **F2:** The short fires on every up day in the profile, including tiny ones: the share of bars with a negative forecast is 1.0 for every rise above 0 in usual moves. The smallest rises (0–0.5 usual moves) are 118 of the 225 short cases at 3 days, and they are followed by +0.77 % excess (t 0.69, 60 days), so those shorts lose. Rises of 0.5–1 usual moves are followed by -1.62 %, and rises above 1 usual move by -2.97 % (t -1.36, 24 days, strength -0.32).
- **F3:** The forecast's size does not track the rise: because the ratio is standardised against its own past 60 values, the two largest entry-forecast quartiles lost -4.28 % and -3.47 % net per trade, while the second quartile earned +0.83 %. The book bets most where the idea's own measure is not largest.
- **F4:** The give-back is much larger in deeper declines. For rises above 0.5 usual moves with a 60-day return below -30 %, the 3-day excess is -5.62 % (t -2.94, 42 cases on 17 days, strength -0.65), against -3.67 % (t -1.39, 15 days) with a 60-day return between -10 % and -30 %. Depth alone is not the effect: in the same deep declines without a sizable rise (0.5 usual moves or less) the coin returns +2.25 % (t 1.17, 33 days), which a short would lose.
- **F5:** The fade grows with the horizon. For rises above 0.5 usual moves, the excess is -2.21 % over 3 days (t -1.37, 52 days) and -4.03 % over 5 days (t -2.41, 25 cases on 14 days, strength -0.31). Rises of 0.5–1 usual moves are followed by -8.7 % over 10 days (9 cases, t -4.75). Each of these moves is 10 to 40 times the 0.22 % cost of a trade.
- **F6:** The effect lives in the profile. Outside the falling agitated market, 3-day excess after rises above 1 usual move ranges from -1.0 % to +1.0 % with no t beyond 1.8. Over 5 days, rises above 2 usual moves continue upward (+7.9 %, t 2.70, 41 cases).

## Ideas
- `058-01.g2.b1.d1_raw-sized-one-day-rise-fade` (from F2, F3, F1): In a falling, agitated market, the larger a coin's one-day rise measured directly in standard deviations of its daily returns over the past 30 days, the larger the fall in its price over the next 3 days, with small up days carrying almost none of it.
- `058-01.g2.b1.d2_deep-decline-one-day-rise-fade` (from F4, F2): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, and the deeper its 60-day fall, the larger the fall in its price over the next 3 days.
- `058-01.g2.b1.d3_one-day-rise-fades-over-5-days` (from F5, F1, F6): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
