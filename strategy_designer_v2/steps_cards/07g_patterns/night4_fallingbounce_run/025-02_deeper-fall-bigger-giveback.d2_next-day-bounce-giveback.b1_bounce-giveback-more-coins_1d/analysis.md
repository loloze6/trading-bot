---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4607 USD
---
## Findings
- **F1:** In coins whose 90-day return is 0 or above, the size of today's rise predicts the next 5 days, the reverse of the falling-market fade. On up days, the 5-day unusual move rises by 2.30 % for each usual daily move of the rise (t 5.65, 1571 non-overlapping cases, Spearman 0.12). The same slope over 10 days is 3.08 % (t 4.36, 754 cases).
- **F2:** That continuation in rising coins is graded and broad. The 5-day unusual move after a rise of 1–2 usual moves is +1.99 % (t 2.89, n 365), after 2–3 moves +4.35 % (t 2.98, n 95), and after more than 3 moves +12.1 % (t 1.90, n 65). Rises above 1 usual move are followed by positive means in 7 of 8 years (2025 is the exception, −0.90 %) and in 79 % of the 19 coins.
- **F3:** In coins with a negative 90-day return, the bounce fade lasts beyond the single day the book held. The 3-day unusual move is −1.03 % after rises of 1–2 usual moves (t −3.09, n 477) and −1.87 % after 2–3 moves (t −2.75, n 129). The 5-day unusual move is −2.38 % after 2–3 moves (t −1.64, n 70) and −7.43 % after more than 3 moves (t −3.65, n 27). These are many times the 1-day sizes the test captured: −0.66 % and −1.28 % next day, against a cost of 0.22 % per trade.
- **F4:** The one-day fade is graded and is opposite in the two regimes. Among up days, the next-day unusual move slopes −0.25 % per usual move in falling coins (t −3.81, n 7482) and +0.20 % per usual move in rising coins (t 4.38, n 8337). The next-day mean after rises above 2 moves runs from −1.62 % (t −2.45) in the lowest 30-day-return quintile to +0.68 % in the highest.
- **F5:** Over the same holding periods, a coin's 30-day return measured in its usual moves predicts its next 10 days. The slope is 1.26 % per unit (t 4.13, 2645 cases) and the 5-day slope is 0.66 % (t 4.24, 5363 cases). It reverses in 2018 (t −4.69) and 2022 (t −3.33), so it is less steady than F1.
- **F6:** The tested book earned nothing, −0.004 % a day on average, with window means scattered from −0.116 % to +0.088 % a day. Its 1-day total move per case of +0.19 % is below the 0.22 % cost of a trade.
- **F7:** Next-day unusual moves alternate by weekday: positive on Tuesday, Thursday and Friday (t 3.3, 2.9, 4.2), negative on Monday, Wednesday and Sunday (t −2.8, −2.5, −2.4). The alternating shape is implausible and many angles were examined, so I treat this pattern as not distinguishable from chance and base no idea on it.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins.g1_breakouts-continue-in-uptrends` (from F1, F2, F4): In a coin whose 90-day return is positive, the larger today's one-day rise measured in usual daily moves, the larger the coin's further rise over the next 5 days.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins.g2_bounce-giveback-over-days` (from F3, F4, F6): In a coin whose 90-day return is negative, the larger today's one-day rise measured in usual daily moves, the larger the coin's fall over the next 5 days.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins.g3_volatility-scaled-monthly-momentum` (from F5, F4): The larger a coin's 30-day return measured in its usual daily moves, the larger its move in the same direction over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
