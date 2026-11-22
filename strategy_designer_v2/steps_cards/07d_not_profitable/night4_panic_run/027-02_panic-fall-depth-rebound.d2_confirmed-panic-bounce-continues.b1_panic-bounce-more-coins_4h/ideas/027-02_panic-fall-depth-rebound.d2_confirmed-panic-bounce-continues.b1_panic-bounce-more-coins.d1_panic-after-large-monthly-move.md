---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's absolute 30-day return before the stretch, in either direction, the higher its return over the following 14 days.
Consequence: A trader buys a panic more heavily the more the coin had already moved over the preceding month, and refuses panics that arrive after a quiet month.
Why:
- F3: The 30-day move before the panic grades what follows better than the bounce does: the slope of the excess 14-day return on the absolute prior 30-day return is t 2.19 on 345 cases; by quartile of that absolute move the excess goes −3.3 %, −0.2 %, +2.9 %, +3.5 % (total −0.5 % to +6.5 %).
- F4: That premium sits at both ends of the prior move: the most-down quintile of the prior 30-day return has +2.8 % excess and the most-up has +4.8 %, while the middle quintiles have −2.3 % and −2.2 %; the signed slope is weaker (t 1.58).
- F2: The bounce carries no graded premium: over 428 panic cases, the excess 84-bar return by bounce quintile goes +0.4 %, −1.0 %, −2.2 %, +0.4 %, +2.6 % (slope t 1.47), and the two lowest quintiles, which the forecast's clip at 0 leaves flat, still had a total 14-day move of +3.3 % and +1.6 %.
- F6: Cost is not the cause: the cases' total move of +1.68 % is 7.5 times the 0.22 % cost of a trade and the 1,092 trades net +3.43 % each (t 3.5, held 13.8 days), but the unusual move per case is −1.28 % (strength −0.041), so the book earns the coins' drift on a fifth of the days and no premium.
