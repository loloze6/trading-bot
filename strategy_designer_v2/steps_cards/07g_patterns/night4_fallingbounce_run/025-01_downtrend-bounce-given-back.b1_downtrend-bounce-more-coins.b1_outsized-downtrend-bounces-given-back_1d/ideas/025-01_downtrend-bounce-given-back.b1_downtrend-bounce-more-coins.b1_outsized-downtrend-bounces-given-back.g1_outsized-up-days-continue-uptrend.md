---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days, and the more usual daily moves the rise covers, the larger the further rise.
Consequence: A trader would buy outsized up days in rising coins, scaled by the rise in usual moves, rather than fade them.
Why:
- F1: In coins whose 90-day return is positive, a large one-day rise is followed by a further rise over the next 5 days, not a fall. On days above 2 usual daily moves the winsorised unusual move is +5.06 % (t 3.96, 103 independent cases, 68 % of cases up). Between 1.5 and 2 moves it is +1.99 % (t 2.21, 163 cases). The link is graded across up days (Spearman 0.124, p < 0.0001, 1,636 cases).
- F2: The answer to a large up day depends on the 90-day trend. Up days above 2 moves end 5 days later lower in falling coins than in rising ones (Welch t −4.68). Up days above 1 move average +1.76 % in rising coins against −2.30 % in falling ones. That mean is positive in 84 % of the 19 coins when rising and in only 21 % when falling. In rising coins it is positive in 7 of 8 years, missing only 2025.
