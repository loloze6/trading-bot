---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day, only while its 30-day return is negative, the fall growing the deeper that 30-day decline.
Consequence: Short bounces only in coins still falling over the past month, and size the short by how deep that month's fall is, so each trade captures a move several times its fee.
Why:
- F1: The book's own gain does not cover what it pays to trade: before fees its positions earned a summed +0.33 over all bars, against −3.48 of fees, and on the signal bars alone +0.61 of gain against −1.90 of fees. Per case the total move (+0.19 %) is only 0.8 times the 0.22 % cost of a trade, so the failing Sharpe (−0.15), mean daily return (−0.00004) and Calmar (−0.07) follow directly from a move too small for its fee.
- F2: The move after a bounce depends on the coin's 30-day return, not on the bounce's size. On cases with forecast ≤ −2, the lowest fifth of 30-day return (below −22 %) gave a next-day unusual move of +0.78 % (t 2.67, 524 cases) and the second fifth +0.68 % (t 3.73, 523). The top two fifths gave −0.06 % (t −0.33) and +0.13 % (t 0.60), and their 3- and 5-day moves were negative (−0.5 % to −0.7 %).
- F6: Scoring each case by the 30-day fall times the bounce size (−r30 × z) orders the move cleanly. The next-day unusual move goes from −0.22 % (t −1.21) in the second-lowest fifth to +0.27 %, then +0.58 % (t 3.32), then +0.88 % (t 2.94) in the top fifth, with 523–524 cases each.
- F8: The result is uneven across years. The next-day unusual move was +0.65 % (t 1.88) in 2018, +0.77 % (t 3.23) in 2019 and +0.62 % (t 3.70) in 2022. It was −0.06 % in 2020, −0.09 % in 2021 and −0.27 % (t −1.63) in 2023, which drives the failure with one window left out (−0.31).
