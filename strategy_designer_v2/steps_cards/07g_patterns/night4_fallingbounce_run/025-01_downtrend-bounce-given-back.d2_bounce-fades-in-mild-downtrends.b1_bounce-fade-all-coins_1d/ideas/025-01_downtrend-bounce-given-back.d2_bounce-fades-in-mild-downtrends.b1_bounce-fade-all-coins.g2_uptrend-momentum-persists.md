---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, its 20-day return measured in usual 20-day moves is followed over the next 5 days by a move in the same direction, larger the further that 20-day return sits from zero.
Consequence: A trader would lean long the rising coins with the strongest recent 20-day runs and refuse to short them.
Why:
- F2: In rising coins, the 20-day return scaled by its usual move predicts the next 5 days in the same direction (slope +0.0070, t 2.64, 2953 cases). Grouped by grid date across coins, the top quintile earns +2.07 % (t 2.06) and the bottom quintile -1.05 % (t -1.16), rising steadily from bottom to top. In falling coins the slope reverses (-0.0053, t -2.54), but its date-grouped quintiles are not ordered.
- F4: The book lost because it shorted against the coins' normal drift, which is -0.74 % per case in the short direction, and its largest bets lost most. Short trades entered at the strongest forecasts (mean -19.5) lost -3.96 % gross on average over 2114 trades, against -0.44 % for the weakest. Its worst years were the rising ones: Sharpe -2.47 in 2020 and -1.99 in 2023, while holding earned +0.45 % and +0.32 % a day.
