---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day, the fall growing with that day's volume against its 20-day average volume.
Consequence: A bounce on heavy volume in a falling coin is the one to short; a quiet bounce carries too little giveback to pay for the trade.
Why:
- F1: The book's own gain does not cover what it pays to trade: before fees its positions earned a summed +0.33 over all bars, against −3.48 of fees, and on the signal bars alone +0.61 of gain against −1.90 of fees. Per case the total move (+0.19 %) is only 0.8 times the 0.22 % cost of a trade, so the failing Sharpe (−0.15), mean daily return (−0.00004) and Calmar (−0.07) follow directly from a move too small for its fee.
- F3: In coins in the lowest third of 30-day return, the fade grows with the day's volume against its 20-day average. The next-day unusual move rises from +0.26 % (t 0.78, 337 cases) in the low-volume third to +0.81 % (t 2.81, 288) in the middle third and +1.52 % (t 3.62, 247) in the high-volume third. In that high-volume third the total move is +1.38 %, about 6 times the 0.22 % cost.
- F4: Across all cases, the top quartile of relative volume (above 1.57× its 20-day mean) gave +0.89 % (t 4.18, 722 cases), against −0.01 % to +0.30 % in the other quartiles.
- F5: Grading by the bounce score alone does not order the move. By the forecast, the −15 to −10 group lost −0.31 % (t −1.35, 382 cases) between groups that gained, and the larger-|forecast| half trailed the smaller half by −0.20 %. Only the top fifth of the raw volatility-scaled rise (above 1.77 usual moves) stood out, at +0.85 % (t 3.86, 573), while the other fifths sat at +0.16 % to +0.28 %.
