---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 7-day return has been positive, the rise over the next day after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the higher the coin's hourly volatility over the last 7 days stands against its volatility over the last 30 days.
Consequence: A fall into settlement is a reason to be long for the next day only when the coin has risen over the past week, so the book stays out after weekly declines.
Why:
- F6: The 7-day trend gives the same split as the 30-day trend. For strong cases with a positive 7-day return the excess is +0.30 % over 24 hours (t 3.31, 2677 cases) and +0.87 % over 72 hours (t 3.29, 938 cases). With a negative 7-day return it is −0.09 % and −0.11 %.
- F2: The book loses its gain in downtrends, which pulls it below holding (Sharpe minus holding −0.13). On bars in a position it earns 0.16 bp per bar when the 30-day return is negative and 0.86 bp when positive, with about the same allocation (0.52 vs 0.54). The uptrend bars carry 9.92 of its 11.77 summed bar gain, so 84 %.
- F3: The 30-day uptrend is not an effect of its own. On settlement bars without the signal (forecast < 2) it earns +0.04 % (t 0.60, 3859 cases) over 24 hours and −0.12 % (t −0.50, 1274 cases) over 72 hours. With the signal the same bars earn +0.24 % and +0.92 % (F1). This fits the brief's theory: after a run up, longs are the crowded, paying side, so the pre-settlement fall is the flow that reverses.
- F7: The book's falls are close to the coin's own falls, which is why Calmar fails (0.15 against 0.75). The book is in a position on 72 % of bars, although the forecast is positive on only 4 % of them, because trades last 38 to 61 hours. Its window falls nearly match the coin's: w20 −29 % vs −29 %, w24 −34 % vs −39 %, w2 −43 % vs −58 %.
