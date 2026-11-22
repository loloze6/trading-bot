---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 to 10 days. The larger the rise in usual moves, the larger the rise that follows.
Consequence: A trader would buy large up days in coins that are not in a 90-day fall, and refuse to short them as bounces.
Why:
- F1: In coins not in the falling regime (90-day return not negative), large one-day rises are followed by further rises rather than falls. On the 5-day grid, rises of more than 2 usual daily moves are followed by an unusual move of +8.55 % (t 2.62, n 133), and rises of 1 to 2 usual moves by +1.74 % (t 2.77, n 408). The slope of 5-day strength on the size of the rise (z>0) is +0.218 (t 6.03, n 1623). The effect holds in both halves of the sample (<date> +5.8 %, t 1.99, n 146; <date> +2.5 %, t 3.65, n 395) and is positive in 79 % of the 19 coins.
- F2: The continuation in F1 is graded and lasts past 5 days. Strength after rises of more than 2 usual moves is 0.11 at 1 day (t 2.29, n 648), 0.28 at 3 days (t 2.78, n 207) and 0.62 at 10 days (t 3.13, n 74). This is 7 to 15 times the 0.04 strength of the tested idea, and the total move is far above the 0.22 % cost of a trade.
- F3: In falling coins, rises do fade, as the tested idea says, but unevenly over time. Five days after rises of more than 2 usual moves the unusual move is -3.76 % (t -2.71, n 79), and the slope of strength on rise size is -0.094 (t -2.49, n 1409). After rises above 1 usual move, the move is -2.4 % in <date> (t -3.22, n 285) but +2.4 % in <date> (t 1.77, n 90). Only 32 % of coins show a positive move after such rises, so the fade holds in most coins, but not in every period.
