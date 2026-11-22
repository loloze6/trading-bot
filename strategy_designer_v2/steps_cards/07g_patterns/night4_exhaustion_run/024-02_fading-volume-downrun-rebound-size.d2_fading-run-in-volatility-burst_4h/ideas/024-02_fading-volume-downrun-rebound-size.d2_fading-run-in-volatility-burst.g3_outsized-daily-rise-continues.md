---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin rises over one day by much more than its usual 1-day move over the past 30 days, it keeps rising over the next three days, and the larger that 1-day rise relative to its usual move, the larger the further rise.
Consequence: A trader refuses to fade an outsized 1-day rally and instead takes the continuation bet.
Why:
- F5: Large 1-day rises are followed by a further rise rather than a give-back. The top size quintile on the up side earns +1.00 % over 3 days (t 2.25, 511 cases, strength 0.116), and the top decile +0.98 % (t 2.19, 501 cases). This is positive in 7 of 8 years.
- F1: The coin's 1-day move, measured against its usual 1-day move over the past 30 days, predicts the next 3 days far better than the tested forecast does. In the top quintile of the move's size, falls are followed by a 3-day excess return of +1.27 % (t 3.50, 490 independent cases, strength 0.145), and the response is graded across the whole down side (Spearman 0.113, p 1.9e-8, n 2450). The tested forecast's active cases earn +0.24 % (t 0.73, 638 cases), and step 5 found -0.01 % per case.
