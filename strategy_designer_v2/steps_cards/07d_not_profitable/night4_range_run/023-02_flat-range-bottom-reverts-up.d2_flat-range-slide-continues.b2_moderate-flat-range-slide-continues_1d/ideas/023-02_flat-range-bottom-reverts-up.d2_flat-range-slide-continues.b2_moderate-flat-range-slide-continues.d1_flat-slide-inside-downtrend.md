---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves and only while its 60-day return is negative, the fall being larger the more negative that 60-day return is.
Consequence: A flat-range slide below the middle is a short to take only inside a coin that has already been falling for two months, and a short to refuse in a coin that is up over two months.
Why:
- F1: The book's loss is mostly the coin's own rise working against a short-only book: per coin, the mean daily book return is between -0.003 % and -0.034 %, and the part due to the market's rise is between -0.009 % and -0.019 % (BTC -0.0168 % against -0.0177 %, XRP -0.0337 % against -0.0177 %), so timing adds about nothing; per case, the total move of +0.12 % over 5 days is only 0.6 times the 0.19 % cost of a trade, because the -0.59 % drift cancels most of the +0.71 % unusual move.
- F2: The idea works only when the coin is already in a 60-day decline: grid cases in the lowest quarter of the 60-day return show an unusual 5-day short-side move of +4.33 % (t 4.27, 47 cases; total move +3.73 %, about 20 times the cost); the third quarter shows -1.44 % (t -1.13). On held bars the position gains +0.027 % and +0.039 % per bar in the two lower 60-day-return quarters (mean 60-day return -38 % and -13 %), and loses -0.125 % and -0.124 % per bar in the two upper quarters (+6 % and +48 %).
- F3: The gain sits in the falling years and turns into a loss in the rising ones: grid-case unusual moves are +2.6 % (t 2.08) in 2018 and +3.1 % (t 3.29) in 2019, but -1.3 % (t -2.02) in 2023 and -1.3 % in 2024; the book's mean daily return is +0.026 % in 2018 and -0.078 % in 2023, a year when the coins averaged +0.15 % a day.
- F5: Holding the short after the signal is gone costs the book: on bars held with the forecast off, the position loses -0.074 % per bar (t -3.25, 4169 bars), against +0.008 % (t 0.16, 2230 bars) while the forecast is on; the 1292 trades that closed with the forecast at 0 lost -1.73 % gross.
