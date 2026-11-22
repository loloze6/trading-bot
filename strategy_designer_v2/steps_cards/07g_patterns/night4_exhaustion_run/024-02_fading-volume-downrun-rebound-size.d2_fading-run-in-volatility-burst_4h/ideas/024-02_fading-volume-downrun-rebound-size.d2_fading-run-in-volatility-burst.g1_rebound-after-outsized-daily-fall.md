---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over one day by much more than its usual 1-day move over the past 30 days, it rises over the next three days, and the larger that 1-day fall relative to its usual move, the larger the rise.
Consequence: A trader buys a coin after an outsized 1-day drop, whatever the streak or the volume behind it, and refuses the rebound bet after ordinary dips.
Why:
- F1: The coin's 1-day move, measured against its usual 1-day move over the past 30 days, predicts the next 3 days far better than the tested forecast does. In the top quintile of the move's size, falls are followed by a 3-day excess return of +1.27 % (t 3.50, 490 independent cases, strength 0.145), and the response is graded across the whole down side (Spearman 0.113, p 1.9e-8, n 2450). The tested forecast's active cases earn +0.24 % (t 0.73, 638 cases), and step 5 found -0.01 % per case.
- F2: The tested idea's streak and volume-fade conditions add nothing. Down-streaks of at least two bars earn +0.16 % over 3 days with fading volume (t 0.47, 628 cases) and +0.37 % with rising volume (t 1.07, 589 cases). The lowest decile of the 1-day move earns +1.23 % (t 3.43, 501 cases).
- F4: The rebound after the largest 1-day falls holds across coins and years. It is positive in 5 of 6 coins (LTC +2.13 % t 2.50, ZEC +2.12 %, XRP +1.66 %, XMR +1.17 %, ETH +1.12 %; BTC -0.20 %). It is positive in 7 of 8 years (2020 +4.20 % t 4.85, 2025 +1.74 % t 2.10; 2019 -1.00 %). This move is about 1.2 % plus the 0.4 % drift, roughly 8 times the 0.19 % cost of a trade.
