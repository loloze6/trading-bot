---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed over the next two days, Monday and Tuesday, by a move in the same direction that grows with the size of Saturday's move. This holds only while the coin's 30-day volatility of hourly returns is low against its own past year, and the calmer the coin, the larger the continuation.
Consequence: A trader would follow Saturday's move into Monday and Tuesday in calm markets only, and stand aside when the coin's recent volatility is high, which is when the book's deep falls occur.
Why:
- F1: The check failed on Calmar alone (0.69 against 0.75). Two long falls cause it: −23.7 % over about 500 days from w10, while the coins rose +20 to +23 %, and −17.0 % over 387 days from w21 (2024–2025), while the coins rose +51 %. The case gains in those years were 2018 +0.03 % (t 0.05), 2021 −0.19 % (t −0.32) and 2025 −0.59 % (t −1.66), against +0.57 % to +1.39 % in 2019, 2020 and 2022–2024.
- F2: The effect lives in calm markets and is absent in turbulent ones. In the low tercile of a coin's 30-day hourly volatility, the Monday–Tuesday move in Saturday's direction averages +1.04 % (t 5.0, 750 cases). In the middle tercile it is +0.30 % (t 1.28, 747) and in the high tercile −0.04 % (t −0.12, 749). The 5 % worst adverse path over the 48 hours goes from −8.1 % in the low tercile to −19.9 % in the high one.
- F3: Low volatility is not an effect of its own. The coins' unsigned 48-hour return on those same Monday bars is only +0.09 % in the low tercile, against +1.04 % when Saturday's sign is followed. It belongs to the brief's own theory: a weekend move made on thin books stands as information when the market is orderly, and is noise when the market is moving violently anyway.
- F4: A weekly book that trades only the low-volatility tercile has a Calmar of 1.82 (deepest fall −5.2 %, yearly +9.4 %, weekly Sharpe 1.23). Low and middle terciles together give Calmar 0.97 (deepest fall −13.3 %, yearly +12.9 %). The full book gives Calmar 0.70 (−24.4 %, +17.1 %).
