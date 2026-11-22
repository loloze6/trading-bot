---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 14 days, only while the coin's absolute 30-day return before the stretch is large, the effect growing with that 30-day move.
Consequence: A trader buys the bounce after a panic only once the coin has moved a lot over the past month, and sizes up with both the bounce and that move.
Why:
- F3: The 30-day move before the panic grades what follows better than the bounce does: the slope of the excess 14-day return on the absolute prior 30-day return is t 2.19 on 345 cases; by quartile of that absolute move the excess goes −3.3 %, −0.2 %, +2.9 %, +3.5 % (total −0.5 % to +6.5 %).
- F2: The bounce carries no graded premium: over 428 panic cases, the excess 84-bar return by bounce quintile goes +0.4 %, −1.0 %, −2.2 %, +0.4 %, +2.6 % (slope t 1.47), and the two lowest quintiles, which the forecast's clip at 0 leaves flat, still had a total 14-day move of +3.3 % and +1.6 %.
- F1: Holding the coin is what fails the book: it is in a position on only 21.7 % of coin-days, earns 0.0055 % a day on the other 29,164 coin-days where the coins rose 0.079 % a day, and earns 0.090 % a day on its 8,091 in-position days where the coins rose 0.41 % a day; the result is a mean of 0.014 % a day and a Sharpe 0.31 below holding's.
- F5: The Calmar failure (0.099) comes from one long fall of −37.8 %: the chained book drops by −32 % to −38 % across w14–w20, starting in w14 where the book lost 0.196 % a day against the coins' −0.43 %, whereas no window before w14 falls deeper than −17.8 %.
