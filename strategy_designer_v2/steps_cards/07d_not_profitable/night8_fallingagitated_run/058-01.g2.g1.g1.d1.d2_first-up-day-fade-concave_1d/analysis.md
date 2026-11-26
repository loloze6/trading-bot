---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d
idea tested: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5891 USD
---
## Findings
- **F1:** The Calmar check failed (0.56 against 0.75) because of one squeeze. The book's deepest fall was −6.0 % over 5 days, all in w14, and one day of it cost −5.92 % while holding the coins gained +11.0 %. On that day 7 of the 9 worst shorts were in w14: each coin rose +10 % to +12 % the next day, at positions of −0.27 to −0.69, against a yearly return of only +4.4 %.
- **F2:** The w14 squeeze cases looked alike. Their up day had a wide range (mean 1.58 in 30-day standard deviations, up to 2.44) and closed near its high (close position 0.75 to 0.99). They came after a deep fall (prior 3-day return −1.77 standard deviations on average, price 36 % below its 20-day high). In short, they were clean breakout days, not intraday spikes that faded.
- **F3:** The fade depends on how much of the day's range the close-to-close rise covers (the rise in standard deviations over the range in standard deviations). By quartile, the next-day short return on signal days is:
- **F4:** The close's place in the day's range tells the same story. Signal days that closed in the lower 60 % of their range were followed by a 1.80 % short return (t 3.10, 83 cases). Those that closed in the top 14 % gave 1.20 % (t 1.71, 72 cases). The same low close without the signal is followed by a rise: short return −1.19 %, t −4.98, 546 cases. The weak close is therefore not an effect of its own.
- **F5:** A rebuilt book on folds B and C confirms the gain. Leaving out the shorts whose rise covered more than about two-thirds of the range:
- **F6:** The range itself is not the problem; the effect is large enough to trade. The widest-range quartile (1.65 to 5.09) carries the largest fade, 2.14 % (t 3.57), and the largest positions (|allocation| 0.36 to 1.20) earn 1.92 % (t 3.61). Both groups also hold the worst loss, −8.3 %. The total move per case is 4.2 times the 0.19 % cost of a trade.

## Ideas
- `058-01.g2.g1.g1.d1.d2.d1_first-up-day-upper-wick-fade` (from F1, F2, F4, F6): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The fall is larger the wider that day's low-to-high range against the standard deviation of its daily returns over the past 30 days, and the further its close sits below the day's high.
- `058-01.g2.g1.g1.d1.d2.d2_first-up-day-rise-share-fade` (from F1, F3, F5): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The fall is larger the wider that day's low-to-high range against the standard deviation of its daily returns over the past 30 days, and the smaller the share of that range its rise from the previous close covers.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
