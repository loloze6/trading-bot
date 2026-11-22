---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour return over Saturday and Sunday is followed by a larger opposite move over the next two days than a 48-hour return of the same size that ends on any other weekday, only for the part made on Sunday: the larger the coin's 24-hour return over Sunday, the larger the opposite move over Monday and Tuesday.
Consequence: A trader would fade Sunday's own move into the week and ignore Saturday's, which removes the half of the weekend return that currently turns the bet into a losing one.
Why:
- F1: The book loses before costs, so the cost is not what sinks it: its 3925 trades of about 45 hours average -0.41 % before fees and -0.51 % after; shorts lose -1.05 % and longs gain +0.37 %; the book loses most on Mondays (-6.2 bp a day) and Tuesdays (-9.2 bp); its Sharpe is -0.66, its mean daily return -0.029 % and its Calmar -0.16; the idea's size is -0.24 % per case against a cost of 0.19 % a trade.
- F2: The 48-hour weekend return joins two halves that act in opposite ways. Across 2387 Monday-00:00 cases, Saturday's 24-hour return correlates +0.071 with the next 48 hours (t 3.47), while Sunday's correlates -0.083 (t -4.06). The full 48-hour return the book trades on correlates only -0.013 (t -0.62), so the two halves cancel.
- F3: Sunday's own 24-hour return is reversed: over the next 24 hours the unusual move against it averages +0.38 % (t 3.42, 2387 cases, strength 0.077), and over the next 48 hours +0.58 % (t 3.85). That is about 2 and 3 times the 0.19 % cost of a trade.
- F4: Sunday's reversal grows with the size of Sunday's move. Over the next 24 hours it is -0.04 % in the smallest |z| quintile (mean |move| 0.34 %), then +0.34 %, +0.33 % and +0.40 %, and +0.86 % in the largest quintile (mean |move| 7.5 %, t 2.63, 478 cases). Over 48 hours the largest quintile reaches +1.09 %.
- F6: Sunday's reversal is broad but not steady. It holds in all six coins over 24 hours (+0.14 % in BTC to +0.58 % in XMR, t 2.38). It is larger after rises (+0.52 %, t 3.48) than after falls (+0.22 %, t 1.38). It was strong in 2019 to 2020 (+0.78 % and +0.85 %) and near zero in 2023 and 2025 (-0.02 % and -0.00 %).
