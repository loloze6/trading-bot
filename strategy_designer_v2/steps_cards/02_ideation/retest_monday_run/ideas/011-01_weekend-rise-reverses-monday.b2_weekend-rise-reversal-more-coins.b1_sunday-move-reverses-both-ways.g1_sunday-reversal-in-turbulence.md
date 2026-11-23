---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close move is undone over the next 2 days (Monday and Tuesday) more strongly the higher the coin's past 20-day volatility stands relative to its usual 60-day volatility, with the larger moves reversing the most.
Consequence: A trader would lean harder against Sunday's move when the coin has recently been turbulent, and lightly or not at all when it has been calm.
Why:
- F1: The Sunday reversal is concentrated in turbulent stretches. Cases were split into thirds by the coin's 20-day volatility relative to its earlier 60-day volatility. In the wildest third, Sunday's move is undone by 1.38 % over Monday and Tuesday (t 5.77, 1148 cases). In the calmest third it is undone by 0.52 % (t 2.38, 1201 cases). The difference, wild minus calm, is 0.85 % (Welch t 2.62).
- F2: The effect belongs to Sunday, not to turbulence in general. In the wild third, Sunday's reversal minus the other weekdays' 2-day reversal is 1.38 % (Welch t 5.41). No other weekday's wild third reverses by more than 0.82 % (Monday, t 3.52), and Friday's wild third continues by 0.44 % (t -2.45).
- F4: The reversal is spread over both days of the hold and grows with the move. Monday alone gives 0.48 % (t 5.51) and Tuesday alone 0.43 % (t 5.55). The size-weighted measure rises from 0.09 % in the smallest fifth of |Sunday z| to 1.55 % in the largest fifth. The 2-day Saturday+Sunday move carries no reversal (product t 1.22), so the effect belongs to Sunday's own bar.
