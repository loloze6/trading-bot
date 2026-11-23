---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), the larger the weekend move the larger the move back, only while the coin's daily volatility over the last 20 days is high against its last 60 days.
Consequence: A trader would lean against Sunday's move only when recent volatility has risen above its longer norm, and stay out of the weekend bet in calm or settling markets, where the reversal is too small to carry the falls.
Why:
- F1: The check failed on Calmar alone: 0.33 against the 0.75 rule, a yearly return of +9.4 % against a deepest fall of −28.7 %. That fall lasted 907 chained days, from w1 to w9, through losing windows w2 (−7.8 %), w3 (−5.7 %), w4 (−3.4 %) and w7 (−4.9 %). Every other measure passed, including a Sharpe of 0.61.
- F2: The effect lives almost entirely in Sundays where the coin's 20-day volatility is high against its 60-day volatility. In the top tercile of that ratio the reversal in the forecast's direction is +1.51 % over 2 days (t 5.07, 879 cases). In the middle and low terciles it is only +0.27 % (t 1.00) and +0.35 % (t 1.53). The book's summed position gain is +6.92 in the top tercile against −0.22 and −0.24 in the other two.
- F3: The high-volatility condition is not an effect of its own. On non-Sunday bars in the same top tercile, a 1-day move reverses by only +0.04 % over 2 days (t 0.25, 2750 cases). The Sunday reversal exceeds it by 1.47 % (Welch t 4.42). This fits the brief's theory: a weekend imbalance in an already stressed, thin book is paid more for liquidity.
- F4: Trading only the top-volatility-ratio Sundays roughly halves the falls in a weekly chained proxy of the book. The deepest fall goes from −15.4 % to −8.2 % with an almost unchanged yearly return (+15.6 % against +15.1 %), lifting the proxy Calmar from 0.98 to 1.90. This proxy is pooled case gains, not the daily book.
- F7: Both sides of the bet reverse, so neither side should be left out. Betting against weekend rises gives +0.77 % (t 4.99, 2574 cases) and betting against weekend falls gives +0.55 % (t 3.75, 2664 cases).
