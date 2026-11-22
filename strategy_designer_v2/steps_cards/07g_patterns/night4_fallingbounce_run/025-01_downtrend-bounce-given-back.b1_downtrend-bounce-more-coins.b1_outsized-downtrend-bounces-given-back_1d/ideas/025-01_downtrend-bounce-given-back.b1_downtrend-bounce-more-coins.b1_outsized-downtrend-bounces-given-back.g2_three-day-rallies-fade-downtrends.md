---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, the larger its 3-day return measured in units of its 20-day standard deviation of daily returns, the larger its fall over the next 5 days.
Consequence: A trader would short falling coins after multi-day rallies, scaled by the 3-day rally in usual moves, instead of reacting to a single day's bounce.
Why:
- F3: In falling coins, the 3-day return measured in usual moves predicts the next 5 days better than the one-day bounce the tested idea uses. The winsorised unusual move falls steadily across 3-day quintiles: +0.11 %, −0.44 %, −0.46 %, −1.02 %, then −1.70 % in the top quintile (t −3.69, 509 cases). The one-day measure is weaker: Spearman −0.065 (p 0.015, 1,414 cases), and its 1.5 to 3 move buckets have t of only −1.7.
- F6: The one-day result reported in step 5 does not come from the bounce size the forecast grades on. In the falling regime, the 5-day unusual move barely changes by forecast bucket: −1.31 % at forecast −10 or below, −1.00 % between −2 and −10, and −0.53 % when flat (t −1.96, −1.64 and −2.34). The falling regime as a whole drifts below the coins' normal drift.
