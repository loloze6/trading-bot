---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall, the larger the rise, and the rise is larger the further its Sunday close sits below its 50-day average price.
Consequence: Buy weekend falls in coins trading under their 50-day average, more the further below, and refuse those in coins above it, which avoids the trades that carry the book's falls without the rebound.
Why:
- F1: The check failed on Calmar alone (0.568 against 0.75). A yearly return of +14.5 % meets a deepest fall of 25.6 %, built over 48 days from window w1 into w2 while the coins fell 59.5 %. In w2 the 73 active weekend-fall cases lost against the coin's drift (mean excess 3-day return −5.12 %, t −3.17), and in w17 the 30 cases did the same (−7.54 %, t −3.31). The other falls were 13.8 % (w17–w18), 11.7 % (w15–w16) and 10.5 % (w11–w13).
- F2: The rebound comes almost entirely from Sundays that close below the coin's 50-day average. Those 703 cases have a mean excess of +1.56 % (t 4.46) and summed position gains of 12.9; the 96 cases above the average have +0.14 % (t 0.14) and 0.47. A case-book of the below-average cases falls at most 5.1 % against 17.1 % for all cases, a gain-to-fall ratio of 18.0 against 8.6, though the 628 cases too early in their window for a 50-day average drop out of that comparison. The condition alone does not earn: Sundays below the average without the signal have −1.35 % (t −5.05, 827 cases). It belongs to the theory because a weekend sell-off in a coin already under pressure is the one-sided flow a thin book overprices.
- F6: The move per case is far above the cost of a trade, so cost is not why the book fails. The total move is +1.98 %, 8.9 times the 0.22 % cost, and the unusual move is +1.50 %, a strength of 0.17. The book fails on its falls, not on its gain: Sharpe 0.88, 0.27 above holding, with no window decisive (lowest leave-one-out Sharpe 0.78).
