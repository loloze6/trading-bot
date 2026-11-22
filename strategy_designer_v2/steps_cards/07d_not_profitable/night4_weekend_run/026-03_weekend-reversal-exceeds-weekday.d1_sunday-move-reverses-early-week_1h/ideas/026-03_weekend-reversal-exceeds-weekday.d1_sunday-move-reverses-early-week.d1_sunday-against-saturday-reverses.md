---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only for the part of Sunday's move that undoes Saturday's: the larger Sunday's 24-hour return minus Saturday's 24-hour return, the larger the opposite move over the next two days.
Consequence: A trader would fade Sunday's move into the week in proportion to how far it reversed Saturday's, and stay small when the two days moved together, which removes the half of the bets that pay the fee for nothing.
Why:
- F1: All of the book's edge comes from Sundays whose move went against Saturday's. Those 1311 cases gained +1.03 % per case over 48 hours (t 5.30), or +0.36 % per case on the actual positions, summing to +4.70. The 1079 cases where Saturday and Sunday moved the same way gained −0.01 % (t −0.02), or −0.04 % on the positions, summing to −0.38. They pay the 0.19 % trade cost on every bet and add only noise to the falls.
- F2: Regressing the next 48 hours on both days shows they pull in opposite directions. Sunday's 24-hour return reverses (slope −0.154, t −4.09), while Saturday's continues (slope +0.104, t 2.79), over 2355 coin-weeks. Sunday minus Saturday gives a slope of −0.129 (t −5.07); the 48-hour weekend sum gives only −0.024 (t −0.87).
- F3: The edge is graded on Sunday's move minus Saturday's, read in the bet's direction. The 48-hour gain rises across quintiles from −0.23 % (t −0.68) to +0.13 %, +0.79 %, +0.89 % and +1.34 % (t 2.98), about 471 cases each. A pure Sunday reversal with no counter-Saturday is worth nothing.
- F6: The failures show up in the falls and the daily gain. The book's daily chain falls by up to 31.0 % (worst in w13, w12, w9), giving a Calmar of 0.12, and its mean daily return is 0.014 %. Mondays (mean +0.108 %, standard deviation 1.78 %) and Tuesdays (+0.036 %, standard deviation 1.53 %) carry all of the risk. All 40 of the book's worst days fall on Monday (23) or Tuesday (17), so the falls come from the bets themselves, half of them the dead same-direction weekends.
