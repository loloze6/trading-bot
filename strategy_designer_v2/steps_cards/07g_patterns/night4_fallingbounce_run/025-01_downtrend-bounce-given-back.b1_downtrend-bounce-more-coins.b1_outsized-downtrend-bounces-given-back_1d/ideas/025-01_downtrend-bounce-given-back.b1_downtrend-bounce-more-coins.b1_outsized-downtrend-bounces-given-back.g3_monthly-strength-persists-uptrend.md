---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the higher its 30-day return measured in units of its 20-day standard deviation of daily returns scaled to 30 days, the higher its return over the next 5 days.
Consequence: A trader would lean long in rising coins whose last month was strong in usual moves, and lean short in those whose last month was weak.
Why:
- F4: In rising coins, the 30-day return measured in usual moves (its 20-day standard deviation times √30) predicts the next 5 days in the same direction. The winsorised unusual move climbs steadily from −2.51 % in the lowest quintile (t −3.01, 181 cases) to +1.25 % in the highest (t 3.07, 894 cases).
- F2: The answer to a large up day depends on the 90-day trend. Up days above 2 moves end 5 days later lower in falling coins than in rising ones (Welch t −4.68). Up days above 1 move average +1.76 % in rising coins against −2.30 % in falling ones. That mean is positive in 84 % of the 19 coins when rising and in only 21 % when falling. In rising coins it is positive in 7 of 8 years, missing only 2025.
