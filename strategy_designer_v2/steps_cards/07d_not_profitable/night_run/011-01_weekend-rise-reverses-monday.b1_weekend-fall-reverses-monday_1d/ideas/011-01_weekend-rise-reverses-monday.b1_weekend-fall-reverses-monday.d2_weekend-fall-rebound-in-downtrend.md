---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall relative to the coin's usual daily move, the larger the rise. The rise is larger the deeper the coin's fall over the past 20 days.
Consequence: Weekend-fall longs should be leaned on hardest when the coin is already in a 20-day decline, which raises the gain per held day where the book is exposed.
Why:
- F2: Where the book does bet, the bet works. On the 1013 held bars the coin's next-day return averaged 0.0052 (t 2.94), against an all-bar coin mean of 0.0012. The gain was 0.0025 per held bar after sizing, and fees were only about 0.0010 per held bar. The loss is not in the forecast or the fees but in how rarely and how small the book is exposed.
- F3: The reversal is not graded within Sunday falls, so the forecast's linear scaling adds nothing. The deepest Sunday-fall quintile (z −1.13) was followed by a next-day return of 0.0076 and a 2-day return of 0.0063. The milder fall quintile (z −0.38) was followed by 0.0069 and 0.0104. This matches the step-5 slope t of 0.29.
- F6: The weekend-fall reversal was largest when the coin was already in a 20-day decline. Held bars after a mean 20-day return of −22% gained 0.0119 the next day and 0.0164 over 2 days. Bars after a flat 20 days (−2%) gained 0.0045 and 0.0049, and bars after a +25% run gained 0.0082 and 0.0080.
