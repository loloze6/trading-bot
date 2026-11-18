---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-midpoint-continues-down
line: 7.d not profitable
backtest: 010-02_rsi-below-midpoint-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 14 days that a coin's 14-day RSI has spent below its midpoint, the larger the coin's fall over the next 7 days, only while the coin's 14-day volatility is low relative to its own past, and the lower that volatility, the larger the continuation.
Consequence: A trader would scale the RSI-regime position down as the coin's recent volatility rises, because in turbulent stretches the persistence turned into sharp reversals that made the book's deepest falls.
Why:
- F1: The Calmar failed because of one long fall: the book chained in window order fell -61.8% against a yearly return of +28.8%, and its deepest fall ran 414 days through windows w2 to w6 (2022–2023), where the book lost -60.8% while the coins rose +63.0%.
- F6: The book's worst 5% of days were sharp reversals against a trend already in place. Shorts lost -5.7% on days the coin rose +7.9% after a 28-day fall of -10.4% (132 days). Longs lost -5.6% on days the coin fell -7.1% after a 28-day rise of +18.6% (158 days).
- F7: In the highest 14-day volatility quartile both sides lost: shorts -0.089% a day (712) and longs -0.023% a day (541). The lower quartiles earned +0.002% to +0.099% for shorts and +0.144% to +0.302% for longs.
