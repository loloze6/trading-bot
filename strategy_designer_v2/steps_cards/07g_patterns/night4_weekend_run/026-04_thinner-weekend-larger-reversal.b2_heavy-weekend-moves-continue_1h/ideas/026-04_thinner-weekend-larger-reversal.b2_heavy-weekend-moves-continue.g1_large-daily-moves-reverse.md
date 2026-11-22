---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour move, its price moves back against that move over the next 24 hours, and the larger the 24-hour move is against the coin's usual daily move, the larger the reversal.
Consequence: A large one-day move is a reason to fade it for the following day rather than chase it.
Why:
- F1: A large move over the past 24 hours, read at 23:00 UTC on any day, is partly reversed over the next 24 hours, and more so the larger the move. In the top fifth of each coin's absolute 24-hour moves the signed next-24-hour return minus drift is −0.50 % (t −4.53, 3208 cases). In the fourth fifth it is −0.20 % (t −2.28). The three smaller fifths sit between −0.02 % and +0.03 % (|t| < 0.4). The top-fifth reversal is about 2.6 times the 0.19 % cost of a trade.
- F2: The reversal of large 24-hour moves (top two fifths) holds broadly but fades in the last two years. It is negative in every window group: w1-8 −0.56 % (t −5.14), w9-16 −0.29 % (t −2.35), w17-24 −0.25 % (t −1.92). It is negative in every year from 2018 to 2023 (t −1.81 to −3.38), and positive in 2024 (+0.11 %, t 0.58) and 2025 (+0.10 %, t 0.54). It is clear in BTC, ETH, LTC and XMR (t −2.04 to −4.48) and absent in XRP (t −0.37) and ZEC (t −0.73).
