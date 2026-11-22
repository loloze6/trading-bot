---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, and the larger that rise in units of the usual daily move, the larger the rise that follows.
Consequence: A sharp up day in a coin that has been rising for months is a reason to be long for the following days rather than to fade it, with more weight the sharper the day.
Why:
- F1: In coins whose 90-day return is not negative, the 5-day unusual move after a day's rise grows with the rise measured in 20-day standard deviations: −0.77 % (t −2.08, 1092 cases) for 0–1 units, +1.42 % (t 1.77, 247) for 1–1.5, +2.31 % (t 2.29, 163) for 1.5–2 and +8.58 % (t 2.65, 134; winsorised +5.91 %, t 4.05; median +2.35 %, 66 % of cases positive) above 2, a strength of 0.55 of the coin's usual 5-day move in the top bucket.
- F2: That grading in rising coins is steady across years and coins: over the 1636 rising-coin up-day cases, the Spearman correlation of the rise with the 5-day unusual move is 0.124 and stays between 0.10 and 0.14 when any one year is left out; 17 of 19 coins have a positive median after rises above 1.5 units; averaged per day it is still +4.65 % with t 2.31 over 126 independent days.
- F4: The book loses on the coins' drift and not on its timing: per bar the position earns −0.0112 %, of which −0.0294 % is the market's own rise against a short held on 44 % of the bars, while timing adds +0.0182 %. That matches step 5's size: total move −0.14 % per case against a cost of 0.22 %.
