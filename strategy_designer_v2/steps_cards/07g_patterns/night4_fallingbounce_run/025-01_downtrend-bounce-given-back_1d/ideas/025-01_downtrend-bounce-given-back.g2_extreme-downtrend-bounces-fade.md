---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise of the very largest size relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the further that rise lies beyond the coin's ordinary large rises, the larger the fall.
Consequence: Only the most extreme bounces in a long-falling coin justify a short over the following days, not every sharp rise.
Why:
- F3: Large rises (above 1.5 usual moves) are followed by a 5-day unusual move 5.8 % higher in rising coins than in falling coins (Welch t 3.53; 116 against 68 cases). This is the contrast the brief names as its test.
- F4: Inside falling coins, the fade is not graded. The correlation between the size of the rise and the following 5-day move is -0.005 (p 0.90, n 614). Only the very largest rises fall afterwards: above 2.5 usual moves, -3.3 % (t -2.01, n 14); 1.5 to 2.5 usual moves, -1.6 % (t -1.52, n 54). This matches step 5's failed supporting check (-0.69 %).
