---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3402 USD
---
## Findings
- **F1:** The book is flat almost all the time. It held a position on only 1013 of about 17,500 coin-bars (about 6%), at a mean allocation of 0.46. Its mean daily return was 0.000085, against 0.00119 for holding the coins. This is why the mean daily return, the Sharpe against holding and the Calmar (0.15, a yearly gain of about 3%) all fail.
- **F2:** Where the book does bet, the bet works. On the 1013 held bars the coin's next-day return averaged 0.0052 (t 2.94), against an all-bar coin mean of 0.0012. The gain was 0.0025 per held bar after sizing, and fees were only about 0.0010 per held bar. The loss is not in the forecast or the fees but in how rarely and how small the book is exposed.
- **F3:** The reversal is not graded within Sunday falls, so the forecast's linear scaling adds nothing. The deepest Sunday-fall quintile (z −1.13) was followed by a next-day return of 0.0076 and a 2-day return of 0.0063. The milder fall quintile (z −0.38) was followed by 0.0069 and 0.0104. This matches the step-5 slope t of 0.29.
- **F4:** Sunday rises are also undone, and the book never trades them. The Sunday rise quintile at z +0.41 was followed by a next-day return of −0.0074 and a 2-day return of −0.0129. The largest rises (z +1.26) were followed by only −0.0011 and −0.0021. The flat middle quintile showed −0.0022 and −0.0005.
- **F5:** The reversal is concentrated after the weekend. On the other weekdays, only the deepest fall quintile (z −1.39) was followed by a next-day rise (0.0056). The other four quintiles were all between −0.0003 and 0.0007. The Sunday quintiles span +0.0076 to −0.0074.
- **F6:** The weekend-fall reversal was largest when the coin was already in a 20-day decline. Held bars after a mean 20-day return of −22% gained 0.0119 the next day and 0.0164 over 2 days. Bars after a flat 20 days (−2%) gained 0.0045 and 0.0049, and bars after a +25% run gained 0.0082 and 0.0080.
- **F7:** The brief's low-volume mechanism is not visible. Next-day returns on held bars were 0.0064, 0.0053 and 0.0068 across Sunday relative-volume terciles of 0.34, 0.63 and 1.36. The gain also failed in 2018 (−0.0055), 2023 (−0.0031) and 2025 (−0.0049).

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways` (from F1, F2, F4, F5): A coin's Monday-and-Tuesday return runs against its weekend (Sunday close-to-close) move: after a weekend rise it falls over the next 2 days, and after a weekend fall it rises over the next 2 days. The larger the weekend move relative to the coin's usual daily move, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d2_weekend-fall-rebound-in-downtrend` (from F2, F3, F6): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall relative to the coin's usual daily move, the larger the rise. The rise is larger the deeper the coin's fall over the past 20 days.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d3_deep-daily-fall-rebounds` (from F1, F5): A coin that fell over the past day rises over the next day, and the larger that fall relative to the coin's usual daily move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
