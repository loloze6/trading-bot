---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is negative, the larger the product of the depth of that 30-day fall and today's rise in usual daily moves, the larger the coin's fall over the next day.
Consequence: A trader would rank bounces by how deep the month's fall behind them is, and short the highest-ranked ones for one day.
Why:
- F2: The move after a bounce depends on the coin's 30-day return, not on the bounce's size. On cases with forecast ≤ −2, the lowest fifth of 30-day return (below −22 %) gave a next-day unusual move of +0.78 % (t 2.67, 524 cases) and the second fifth +0.68 % (t 3.73, 523). The top two fifths gave −0.06 % (t −0.33) and +0.13 % (t 0.60), and their 3- and 5-day moves were negative (−0.5 % to −0.7 %).
- F6: Scoring each case by the 30-day fall times the bounce size (−r30 × z) orders the move cleanly. The next-day unusual move goes from −0.22 % (t −1.21) in the second-lowest fifth to +0.27 %, then +0.58 % (t 3.32), then +0.88 % (t 2.94) in the top fifth, with 523–524 cases each.
- F7: The book keeps positions beyond the 1-day horizon, which costs gain and fees. Trades last 3.4 days on average. Bars where a position was still held with a forecast of 0 or a weak forecast lost −0.17 and −0.10 of summed gain, and the trades out of positions on flat bars cost −1.14 of fees. Gross mean per trade was −1.42 %, with 46.6 % of trades winning after fees.
