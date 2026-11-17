---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and a coin that fell over the weekend rises over those 2 days, only while the coin's 20-day return is negative. The more negative that 20-day return and the larger the weekend move relative to the coin's usual daily move, the larger the move back.
Consequence: Fade weekend moves through Tuesday mainly in coins that have been falling over the past 20 days, and stand aside from fading in coins that have been rising, where the book's losing weekends sit.
Why:
- F2: The reversal the book bets on is real and specific to the weekend. On Sundays the 2-day fade return is 0.79% (t 4.83, n 2021). On the other six days it ranges from -0.33% to +0.08% (t -2.44 to 0.55).
- F3: The book holds only one day of a reversal that runs on into Tuesday. The fade earns 0.45% over Monday (t 4.13), 0.23% more on Tuesday (t 2.39) and 0.64% over the two days (t 4.29, n 2441). Each Sunday's fee of 0.045% of the book takes about 36% of the mean Monday gain of position × return (0.125%).
- F5: The reversal sits in coins whose 20-day return is negative and is weak in rising coins:
- F1: The book is only exposed from Sunday close to Monday close, so it is flat about 71% of days (active share 28.6%). Its mean daily return is 5.6e-05 against the required 5e-04, and only Mondays earn anything: the book's mean is 7.97e-04 on Mondays and about 0 on every other weekday. That gives a yearly return of 1.2% against a deepest fall of 24.5% (Calmar 0.06), with falls of 20–24% in w9, w6, w7, w8 and w13.
