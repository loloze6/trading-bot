---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed over the next two days, Monday and Tuesday, by a move in the opposite direction. This holds only while the coin's 30-day volatility of hourly returns is high against its own past, and the more volatile the coin and the larger Sunday's move, the larger the reversal.
Consequence: A trader would lean against Sunday's move into Monday and Tuesday when the market is volatile, and refuse that trade when the coin is calm.
Why:
- F1: Sunday's 24-hour move is reversed over Monday and Tuesday: across 1910 Sunday cases the de-drifted 48-hour return against Sunday's direction averages +0.84 % (t 5.06, strength 0.131), and it is positive in every year 2018–2025 (from +0.03 % to +1.82 %) and for every coin (from +0.48 % to +1.21 %).
- F2: Sunday's reversal grows with the coin's 30-day volatility of hourly returns: +0.02 % (t 0.10, strength 0.003, 647 cases) in the calmest third, +0.88 % (t 3.51, strength 0.138, 644 cases) in the middle third and +1.65 % (t 4.40, strength 0.257, 619 cases) in the most volatile third. The slope of the 48-hour return on Sunday's raw move has t −3.88 in the most volatile third and +1.16 in the calmest third.
- F3: Inside the two more volatile thirds, larger Sunday moves are reversed somewhat more: by quartile of the size of Sunday's move the reversal is +0.93 %, +1.44 %, +1.10 % and +1.58 % (t 2.6 to 3.1, about 316 cases each, slope t −2.1 to −3.2).
- F5: The reversal is weekend-specific: a weekday's 24-hour move is reversed over the next day by only +0.17 % (t 2.22) in the middle volatility third and +0.12 % (t 1.17) in the top third. A Sunday move in hot markets is reversed by +0.94 % over Monday alone (t 4.39, slope t −3.29), with the hot split taken at the median of 30-day volatility.
