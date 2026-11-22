---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods whose loss is several times its typical four-hour move over the past 30 days, it rises over the next one to three days, whatever the volume did during the streak, only while its 5-day volatility is high relative to its 30-day volatility. The larger that volatility ratio and the larger the loss relative to the typical move, the larger the rise.
Consequence: A trader buys extreme down-streaks only when volatility is expanding, and stays out of calm markets, where these streaks keep falling.
Why:
- F1: The book is the coin held with leverage near one, so its falls are the coin's falls. It holds a long position on 98.6 % of bars at a mean allocation of 0.98, and its daily returns correlate 0.93 with holding. Its deepest fall is −68.7 % against a yearly return of 29.6 % (Calmar 0.43), and its worst windows track the coin's: w14 −50.8 % against −49.4 %, w2 −36.9 % against −44.4 %, w7 −38.0 % against −49.8 %.
- F2: The forecast is positive on only 49.2 % of bars, yet the book is long on 50.0 % of all bars while the forecast is 0. Those bars earn 0.0003 % per 4-hour bar (52,513 bars) against 0.050 % on bars with a positive forecast (51,096 bars). Half the exposure carries the coin's falls without the idea.
- F3: The idea has almost no size. Over 3 days its unusual move is +0.05 % per case (strength 0.007, t 0.48, 5,674 cases), against a trade cost of 0.19 %. Its total move of +0.46 % is mostly the coin's normal drift of +0.41 %.
- F4: The rebound appears only while the coin's 5-day volatility is high against its 30-day volatility. In the top fifth of that ratio (1.20 to 2.36), cases rise +1.05 % beyond drift (t 3.20, 847 cases). In the bottom fifth (0.21 to 0.67), they fall −0.50 % (t −2.08, 847 cases). On long bars the same split gives +0.093 % against −0.004 % per 4-hour bar.
- F6: Only the most extreme streaks carry any effect. Cases with forecasts of 16.5 to 20 gain +0.51 % beyond drift (t 2.75, 2,264 cases). The three lower bands (2 to 16.5) are all negative, from −0.15 % to −0.40 %, so ordinary streaks add exposure without edge.
