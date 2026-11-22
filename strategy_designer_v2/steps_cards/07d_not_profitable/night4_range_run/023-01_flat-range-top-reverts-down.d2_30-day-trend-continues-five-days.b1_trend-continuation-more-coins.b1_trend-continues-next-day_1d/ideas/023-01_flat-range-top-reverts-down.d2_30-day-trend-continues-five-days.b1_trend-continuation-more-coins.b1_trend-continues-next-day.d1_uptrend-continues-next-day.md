---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day, only while that 30-day return is a rise.
Consequence: A trader would follow a coin's 30-day trend upward for the next day, scaled by the size of the rise, and would not short a coin's 30-day fall.
Why:
- F1: The short side is what keeps the book from paying. On 7,684 active short bars the mean move in the position's direction is −0.080 %, against +0.368 % on 7,918 long bars. Rebuilt with the shorts set flat, the book (an approximation: allocation × next-day return, minus 0.11 % per unit of turnover) clears both failed measures: mean daily return 0.000617 against 0.000488 for all bars, Calmar 1.25 against 0.49, Sharpe 1.02 against 0.60, deepest fall −17.8 % against −29.2 %. The shorts alone have a mean of −0.000082, a Sharpe of −0.15 and a deepest fall of −50.1 %.
- F4: Rising coins keep rising at every volatility level, and most strongly when volatility is high against its own past. Longs in the top relative-volatility quartile move +0.724 % (t 4.06, n 1,659), and longs in the top absolute-volatility quartile move +0.507 % (t 2.80).
- F5: The book's worst periods are years with a large short share. In 2018 longs were 17 % of active bars and the move in the position's direction was −0.155 %. In 2025 longs were 37 % and the move was −0.005 %. In 2020 longs were 75 % and the move was +0.307 %.
