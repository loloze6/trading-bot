---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Saturday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Saturday's move, the larger Sunday's move against it.
Consequence: After a large Saturday move, lean against it through Sunday, harder the larger the move.
Why:
- F5: Reversal of a day's scaled move into the next day is not specific to Sunday. The slope of next-day excess return on minus the 20-day z of the move is 45.9 bp per z unit for Saturday bars (t 4.13, n 2069) and 43.7 bp for Sunday bars (t 3.23, n 2069). Tuesday to Thursday bars give 22–34 bp (t 2.1–3.2), while Monday bars continue at −20.5 bp (t −2.27).
- F2: The reversal shows in the earlier years only. Sunday slopes in 2018–2021 are 4.5, 5.9, 11.0 and 6.3 bp per forecast unit (t 1.0, 2.7, 3.4, 1.2, about 258 cases each). In 2022–2025 they are −0.2, 0.5, −0.4 and −1.1 bp (all |t| < 0.4).
