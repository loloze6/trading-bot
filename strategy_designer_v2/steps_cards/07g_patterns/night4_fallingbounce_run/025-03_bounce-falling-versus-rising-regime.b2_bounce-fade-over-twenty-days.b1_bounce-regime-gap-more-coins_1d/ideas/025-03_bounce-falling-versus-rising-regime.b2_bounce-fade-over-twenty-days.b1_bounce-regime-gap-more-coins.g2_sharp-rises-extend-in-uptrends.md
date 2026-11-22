---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin up over its last 90 days, the larger a one-day rise measured in usual daily moves (the day's return over the standard deviation of its last 20 daily returns), the higher its return over the next 5 days.
Consequence: A trader would add to a long after a sharp up day in a coin up over 90 days over the following days, more so the sharper the rise, instead of fading it.
Why:
- F2: In coins up over 90 days, a day's rise is followed by a 5-day continuation that grows with the rise. The unusual 5-day move is −0.55 % after a 0–1 usual-move day (n 1046), +1.99 % after a 1–2 usual-move day (t 2.89, n 365) and +7.50 % after a rise above 2 usual moves (t 2.74, n 160). Across up days the rank correlation of rise size with the 5-day move is 0.12 (p 2e-6, n 1571). Rises above 2 usual moves are positive in both halves: +16.3 % (t 1.70, n 42) in 2018–21 and +4.38 % (t 3.05, n 118) in 2022–25.
- F1: The book's gain comes from long positions in rising coins (trending regime), while its shorts in falling coins lose. Per bar, trending longs earn a mean +0.168 % (t 4.45, 14645 bars, summed +24.6), and mean_reversion shorts lose a mean −0.106 % (t −3.15, 14294 bars, summed −15.2). Short trades entered in mean_reversion average −15.5 % net with a median of −10.1 % (t −19.0, 1907 trades), and they lose in every |entry forecast| quartile (−11.1 % to −17.3 %).
