---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that falls, the coin rises more than usual over the next day, and the larger that day's fall relative to the coin's past 20 days of daily volatility, the larger the next day's rise.
Consequence: A sharp down day, measured against the coin's recent volatility, is a reason to buy for the following day, and a mild one is a reason to refuse the trade.
Why:
- F1: Daily returns reverse on the next day. Over 6 coins and 24 windows (17,119 daily cases), the 1-day return's correlation with the next day's unusual move is -0.082, and the top tertile of 1-day return minus the bottom tertile is -0.094 of a usual daily move (Welch t -4.70). All 6 coins have the negative sign, and 5 of 6 have p ≤ 0.0005 (rho -0.072 to -0.113; ZEC -0.038, p 0.06). Among about 44 feature-horizon pairs examined, this is the one that stands out.
- F2: The reversal is carried by falls and is graded by their size. Scaled by the coin's 20-day volatility, the lowest quintile of the 1-day return is followed by +39.6 bps of unusual move the next day (2,854 cases), the middle quintile by -9.2 bps, and the 4th by -22.0 bps. Within down days the rank correlation is -0.062 (7,002 cases); within up days it is -0.011. The lowest quintile still leads over 2 days (+53.8 bps) and 3 days (+28.2 bps).
- F3: The size covers a trade, but the effect is fading. +39.6 bps of unusual move per case is about twice this backtest's 19 bps round trip, although the spread is uneven by coin (bottom minus top quintile: 120 bps on XMR, t 4.25; 5.7 bps on XRP, t 0.14). The yearly correlation is -0.157, -0.108, -0.147 in 2018-2020 and -0.126 in 2023, but -0.027 in 2024 and +0.002 in 2025. By halves it is -0.107 in w1-12 and -0.051 in w13-24.
