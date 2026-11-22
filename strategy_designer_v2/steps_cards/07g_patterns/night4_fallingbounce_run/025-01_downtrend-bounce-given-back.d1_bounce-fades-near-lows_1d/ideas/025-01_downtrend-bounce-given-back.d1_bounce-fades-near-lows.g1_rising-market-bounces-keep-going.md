---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days, and the larger the rise in standard deviations, the larger the rise that follows.
Consequence: A trader would buy large up days in coins that are rising over the past 90 days, and refuse to short them.
Why:
- F1: In coins whose 90-day return is not negative (regime `unknown`), a large one-day rise is followed by a further rise rather than a giveback. Over the next 5 days the unusual move is +5.5 % (0.48 usual moves, t 2.81, n 59) after rises above 2 of the 20-day standard deviation. It is +1.8 % (0.15, t 2.07, n 170) after rises of 1 to 2. Among up days, the slope of the 5-day move on the rise is +0.185 usual moves per standard deviation (t 3.58, n 781), and the 3-day slope is +0.137 (t 3.64, n 1358).
- F2: Rises above one standard deviation are followed over 5 days by moves 0.225 usual moves larger in rising coins than in falling ones (t 2.28; 229 cases in rising coins, 162 in falling). Across all regimes, the 5-day unusual move after such rises grows with the coin's 20-day return: 0.084, then 0.150, then 0.217 usual moves by tercile (the top tercile t 2.00, n 127).
