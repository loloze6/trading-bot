---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise of several usual daily moves (the day's return over the standard deviation of its last 20 daily returns) is followed by a further rise over the next 10 days, larger the larger the day's rise.
Consequence: A trader would treat a sharp up day in a coin up over 90 days as a reason to be long for the following days, more strongly the sharper the day, rather than as a move to fade.
Why:
- F1: In coins up over 90 days, a one-day rise of at least 2 times the standard deviation of the last 20 daily returns is followed by an unusual move (return minus the coin's normal drift) of +2.56 % over the next 5 days (t 3.05, 274 non-overlapping cases) and +5.97 % over the next 20 days (t 2.41, 193 cases). After the same rises in coins down over 90 days, the unusual move is −0.35 % (t −0.52, 221 cases) and +0.32 % (t 0.13, 148 cases).
- F2: In 90-day risers, the 10-day unusual move after a rise grows with the rise's size: +0.54 % (t 0.51, n 361) for 1 to 1.5 usual moves, +4.35 % (t 2.83, n 228) for 1.5 to 2, and +7.04 % (t 3.02, n 115) for 2 to 2.5. It is +2.35 % (t 1.03, n 70) for 2.5 to 3 and +6.30 % (t 2.04, n 103) above 3. The 5-day bins follow the same ordering, +1.29 %, +2.05 %, +3.07 %, −0.09 % and +4.43 %.
- F3: The 20-day continuation after rises of at least 2 usual moves in 90-day risers is positive in all six coins, from +3.4 % to +9.5 % (largest single-coin t 2.62, ETH). It is positive in 6 of the 8 years and negative in 2022 (−0.7 %, n 5) and 2023 (−2.6 %, n 32).
