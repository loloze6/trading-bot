---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose own 60-day return is positive, a Sunday fall (the Sunday close-to-close return) is followed by a rise over the next 3 days. The rise is larger the larger the fall times the coin's 20-day volatility of daily returns.
Consequence: Buy volatile coins' weekend falls only while the coin's own 60-day trend is up, and refuse them in a falling coin, where the rebound turned into further losses and cut the book's Calmar.
Why:
- F1: The tested rebound is real when pooled but uneven over time. Sunday falls are followed by a 3-day excess of +0.97 % (t 4.67 over 2125 cases, counted per coin and Sunday). Measured per date, no single year reaches |t| 1.4, and the yearly mean ranges from −1.98 % in 2018 (29 dates) to +2.39 % in 2021 (36 dates).
- F2: The years where the rebound failed are the years where the coins fell, and they are where the book lost its Calmar. In 2018, 2022 and 2025 the coins' mean daily return was −0.35 %, −0.26 % and −0.03 %, and the Sunday-fall excess was −1.98 %, −0.44 % and −0.12 %. In 2020, 2021 and 2024, with coin means of +0.47 %, +0.64 % and +0.28 %, it was +1.24 %, +2.39 % and +1.17 %; 2023 is the exception at −0.32 % with a +0.32 % coin mean. The book lost −0.077 % a day in 2018 and −0.069 % a day in 2022, with mean trade returns of −0.60 % and +0.11 % (184 and 643 trades), against +2.7 % to +6.1 % in 2019–2021.
- F3: The coin's 20-day volatility, more than the weekday, carries the rebound. After Sunday falls larger than one daily volatility, the 3-day excess by volatility tercile is −0.14 %, +1.39 % and +3.83 % (126, 146 and 105 cases). Non-Sunday falls of that size in the top tercile also show +1.73 % (t 1.51 over 101 dates, sampled on the non-overlapping grid).
