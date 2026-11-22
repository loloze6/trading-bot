---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound
line: 7.e profitable but not proven
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's own 30-day rise, measured as its plain 30-day return, the more it rises over the next three days beyond its normal drift.
Consequence: A trader holds a long position in a coin in proportion to its raw 30-day rise, and refuses longs in coins with a weak or negative 30-day return.
Why:
- F1: Of the book's mean daily gain on bars of 0.000818, 0.000324 is the market's own rise and 0.000494 is timing; the book earns 0.000742 a day (t 3.18, 2898 days) against 0.001179 for holding, so it beats holding on Sharpe (1.128, 0.574 above holding) and not on mean return.
- F2: The book is not a pullback trade: the idea's regime is active on only 4.8 % of bars, yet the book holds a position on 52.2 % of bars (mean allocation 0.245); its 3476 trades are all long and last 133.6 hours on average, against a planned 72.
- F3: What the book holds is the coin's 30-day trend. Over the next 72 hours, bars with a positive 30-day return show an unusual move of +0.35 % against −0.29 % after a negative one (Welch t 2.49, 2183 and 2101 non-overlapping cases), and the t of this gap is near or above 2 at most horizons from 4 to 240 hours (2.58, 2.70, 2.45, 2.49, 2.06).
- F4: The gain from the 30-day trend is graded at the top. Over 72 hours the unusual move by quintile of the coin's own 30-day return is q4 +0.60 %, q3 +0.24 %, q2 +0.01 %, q1 −0.79 % and q0 +0.13 % (about 858 cases each); over 168 hours it is q4 +1.00 %, q3 +0.44 % and q1 −2.04 %.
- F5: The plan's grading did not work. Inside rising coins, the 30-day rise standardised against its own past 180 values does not rank the next 72-hour move (Spearman −0.005, 1387 cases) or the next 168-hour move (−0.037, 546 cases); the raw 30-day return does rank it (F4).
- F7: The trend side pays in most years and coins but not all. Over 72 hours the trend-signed unusual move is positive in 2019–2021 and 2024–2025 (+0.32 % to +1.22 %) and negative in 2018, 2022 and 2023 (−0.16 %, −0.45 %, −0.18 %); by coin it is positive in five of six (+0.27 % to +0.61 %), with XMR at −0.04 %.
