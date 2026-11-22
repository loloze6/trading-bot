---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin up over its last 90 days, the deeper a one-day fall measured in usual daily moves (the day's return over the standard deviation of its last 20 daily returns), the higher its return over the next 20 days.
Consequence: A trader would treat a sharp down day in a coin up over 90 days as a basis for a long over the following weeks, the stronger the deeper the fall, rather than as a reason to sell.
Why:
- F3: In coins up over 90 days, a one-day fall is followed by a higher 20-day unusual move, larger the deeper the fall. The move is +12.2 % after a fall of 1–2 usual moves (t 3.18, n 82) and +13.1 % below −2 (n 11). By half, falls below −1 give +16.4 % (t 2.75, n 50) in 2018–21 and +7.6 % (t 2.53, n 43) in 2022–25. In both halves the order runs fall below −1 > fall of 0 to −1 > rise: +16.4/+8.3/+1.3 % and +7.6/+2.4/−2.4 %.
- F1: The book's gain comes from long positions in rising coins (trending regime), while its shorts in falling coins lose. Per bar, trending longs earn a mean +0.168 % (t 4.45, 14645 bars, summed +24.6), and mean_reversion shorts lose a mean −0.106 % (t −3.15, 14294 bars, summed −15.2). Short trades entered in mean_reversion average −15.5 % net with a median of −10.1 % (t −19.0, 1907 trades), and they lose in every |entry forecast| quartile (−11.1 % to −17.3 %).
