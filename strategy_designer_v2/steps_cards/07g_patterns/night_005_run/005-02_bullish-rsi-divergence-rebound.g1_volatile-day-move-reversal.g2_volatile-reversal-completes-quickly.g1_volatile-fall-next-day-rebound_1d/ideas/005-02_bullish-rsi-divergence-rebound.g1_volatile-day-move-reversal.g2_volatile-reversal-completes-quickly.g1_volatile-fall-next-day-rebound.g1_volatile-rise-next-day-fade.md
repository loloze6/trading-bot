---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day rise is followed by a fall over the next day. The larger the rise relative to the coin's 60-day mean absolute daily move, the larger that next-day fall.
Consequence: A trader should refuse to chase a big up day in a volatile stretch, and could short it for one day, sized up as the rise grows.
Why:
- F3: The mirror of the tested idea holds: in the high-volatility regime, a day rising more than 2 usual moves (rise / 60-day mean absolute daily move) is followed by a mean excess next-day return of −0.0060 (t −2.35, n 193), and rises of 0.6 to 1.2 usual moves are followed by −0.0048 (t −1.85, n 250); outside the regime, rises above 2 usual moves give −0.0010 (t −0.29).
- F4: The fade after up days is graded but modest: on high-volatility up days, Spearman rho between the sized rise and the next-day excess return is −0.072 (p 0.019, n 1050); it is negative in both halves of the period (large rises −0.0038, t −1.28 early and −0.0046, t −2.29 late) and stronger in ETH (−0.0078, t −2.79) than in BTC (−0.0011, t −0.49).
- F5: The book's gain comes almost entirely from high-volatility bars (summed position gain 2.997 against 0.027 elsewhere); it is in the market only 27.6 % of bars at a mean allocation of 0.40, so its mean daily return of 0.000378 trails holding's 0.00128; timing makes up most of its gain (BTC 0.000436 of 0.000580, ETH 0.000326 of 0.000464).
