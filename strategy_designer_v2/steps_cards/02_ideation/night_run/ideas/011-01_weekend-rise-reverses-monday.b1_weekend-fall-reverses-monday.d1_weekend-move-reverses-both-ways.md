---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Monday-and-Tuesday return runs against its weekend (Sunday close-to-close) move: after a weekend rise it falls over the next 2 days, and after a weekend fall it rises over the next 2 days. The larger the weekend move relative to the coin's usual daily move, the larger the move back.
Consequence: The book could take a position after every weekend, short after a rise as well as long after a fall. That would roughly double how often it is exposed, which is what the failing mean return and Calmar need.
Why:
- F1: The book is flat almost all the time. It held a position on only 1013 of about 17,500 coin-bars (about 6%), at a mean allocation of 0.46. Its mean daily return was 0.000085, against 0.00119 for holding the coins. This is why the mean daily return, the Sharpe against holding and the Calmar (0.15, a yearly gain of about 3%) all fail.
- F2: Where the book does bet, the bet works. On the 1013 held bars the coin's next-day return averaged 0.0052 (t 2.94), against an all-bar coin mean of 0.0012. The gain was 0.0025 per held bar after sizing, and fees were only about 0.0010 per held bar. The loss is not in the forecast or the fees but in how rarely and how small the book is exposed.
- F4: Sunday rises are also undone, and the book never trades them. The Sunday rise quintile at z +0.41 was followed by a next-day return of −0.0074 and a 2-day return of −0.0129. The largest rises (z +1.26) were followed by only −0.0011 and −0.0021. The flat middle quintile showed −0.0022 and −0.0005.
- F5: The reversal is concentrated after the weekend. On the other weekdays, only the deepest fall quintile (z −1.39) was followed by a next-day rise (0.0056). The other four quintiles were all between −0.0003 and 0.0007. The Sunday quintiles span +0.0076 to −0.0074.
