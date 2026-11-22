---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range, the more negative its 60-day return, the more it falls over the next 5 days.
Consequence: A coin that pauses flat for a month after a two-month decline is a short whose expected fall grows with the depth of that decline.
Why:
- F2: The idea works only when the coin is already in a 60-day decline: grid cases in the lowest quarter of the 60-day return show an unusual 5-day short-side move of +4.33 % (t 4.27, 47 cases; total move +3.73 %, about 20 times the cost); the third quarter shows -1.44 % (t -1.13). On held bars the position gains +0.027 % and +0.039 % per bar in the two lower 60-day-return quarters (mean 60-day return -38 % and -13 %), and loses -0.125 % and -0.124 % per bar in the two upper quarters (+6 % and +48 %).
- F3: The gain sits in the falling years and turns into a loss in the rising ones: grid-case unusual moves are +2.6 % (t 2.08) in 2018 and +3.1 % (t 3.29) in 2019, but -1.3 % (t -2.02) in 2023 and -1.3 % in 2024; the book's mean daily return is +0.026 % in 2018 and -0.078 % in 2023, a year when the coins averaged +0.15 % a day.
- F4: The forecast's size does not grade the fall: the most negative forecast quarter has an unusual move of +0.29 % (t 0.39), against +2.30 % (t 2.31) for the third quarter, and the step-5 supporting check gave larger half minus smaller half = -0.77 %.
