---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the rise is larger the larger that fall is measured in units of the coin's usual daily move over its past 60 days.
Consequence: Size weekend-fall buys by how unusual the fall is for that coin, so small routine dips get little capital and the book's losses on them shrink.
Why:
- F3: The size of the weekend fall against the coin's usual daily move grades the rebound strongly, with the Sunday return divided by the 60-day daily standard deviation. The quartile of largest falls returns +3.30 % excess (t 4.79, 172 cases), against +2.20 %, +0.72 % and +0.04 % for the other quartiles. The raw Sunday-return quartiles show the same, from +2.97 % (t 4.46) to −0.06 %. Cases beyond one usual move (145) give +3.29 % (t 4.32), and their case-book falls at most 3.7 %. Sundays with such a fall but no signal earn −1.02 % (t −0.59, 70 cases), so the measure is not an effect of its own.
- F1: The check failed on Calmar alone (0.568 against 0.75). A yearly return of +14.5 % meets a deepest fall of 25.6 %, built over 48 days from window w1 into w2 while the coins fell 59.5 %. In w2 the 73 active weekend-fall cases lost against the coin's drift (mean excess 3-day return −5.12 %, t −3.17), and in w17 the 30 cases did the same (−7.54 %, t −3.31). The other falls were 13.8 % (w17–w18), 11.7 % (w15–w16) and 10.5 % (w11–w13).
- F6: The move per case is far above the cost of a trade, so cost is not why the book fails. The total move is +1.98 %, 8.9 times the 0.22 % cost, and the unusual move is +1.50 %, a strength of 0.17. The book fails on its falls, not on its gain: Sharpe 0.88, 0.27 above holding, with no window decisive (lowest leave-one-out Sharpe 0.78).
