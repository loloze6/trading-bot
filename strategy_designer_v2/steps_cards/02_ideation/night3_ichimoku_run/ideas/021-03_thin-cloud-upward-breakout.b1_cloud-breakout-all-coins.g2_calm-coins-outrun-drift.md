---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The lower a coin's volatility of daily returns over the past 20 days, the higher its return over the next 26 days relative to its normal drift.
Consequence: Calm stretches are where a long bet on a coin earns more than holding it, and agitated stretches are where it earns less.
Why:
- F3: Lower volatility before a cross is followed by a larger 26-day return. At the cross, 20-day volatility has rho -0.242 (p 0.0003, 217 cases); the calmest third ends +12.1 % against drift and the most volatile third -3.0 %. The sign is negative in 10 of 13 coins, and the effect survives the run-up in a rank regression (t -2.42, with the run-up at t -2.04).
- F4: The F3 volatility effect is not specific to the cross, and it is recent. On all 26-day stretches from 2023, 20-day volatility has rho -0.251 (p < 0.0001, 450 cases), and the calmest quintile over all years ends +4.8 % against drift (t 2.11, 155 cases). Up to 2022 the grid shows no such effect (rho -0.038, p 0.46, 375 cases), so this rests mainly on one period.
