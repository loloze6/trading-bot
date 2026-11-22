---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by an opposite move over the next 24 hours, and the larger Sunday's move, the larger that opposite move.
Consequence: If confirmed, a one-day fade of Sunday's move pays about twice the cost of a trade per case and leaves the book exposed for half as long; if rejected, it is a reason to refuse such fades.
Why:
- F3: Sunday's own 24-hour return is reversed: over the next 24 hours the unusual move against it averages +0.38 % (t 3.42, 2387 cases, strength 0.077), and over the next 48 hours +0.58 % (t 3.85). That is about 2 and 3 times the 0.19 % cost of a trade.
- F4: Sunday's reversal grows with the size of Sunday's move. Over the next 24 hours it is -0.04 % in the smallest |z| quintile (mean |move| 0.34 %), then +0.34 %, +0.33 % and +0.40 %, and +0.86 % in the largest quintile (mean |move| 7.5 %, t 2.63, 478 cases). Over 48 hours the largest quintile reaches +1.09 %.
- F6: Sunday's reversal is broad but not steady. It holds in all six coins over 24 hours (+0.14 % in BTC to +0.58 % in XMR, t 2.38). It is larger after rises (+0.52 %, t 3.48) than after falls (+0.22 %, t 1.38). It was strong in 2019 to 2020 (+0.78 % and +0.85 %) and near zero in 2023 and 2025 (-0.02 % and -0.00 %).
