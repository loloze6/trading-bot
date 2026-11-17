---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, only while the coin's 30-day return is positive.
Consequence: Volume-burst falls should be bought only as dips inside a rising market and refused in a falling one, where they keep falling.
Why:
- F5: The losses sit in bear years: falls in 2018 lose −2.66% over 3 days (t −2.24) and falls in 2022 lose −2.75% (t −2.73) and −3.88% over 5 days (t −3.32), while 2020 (+4.17% over 1 day, t 2.95) and 2021 (+1.96%, t 2.22) carry the rebound.
- F6: Falls that come after the strongest 30-day rise (top third of 30-day return, n 114) gain +0.95% over 1 day (t 2.30), while those in the middle third lose −1.77% over 5 days (t −1.98).
- F3: Volume ratio grades the next-day move: the top third by volume ratio gains +1.14% over 1 day (t 1.74, n 148) against −0.04% for the bottom third, but the same top third loses −1.78% over 5 days (t −1.94).
