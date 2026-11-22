---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise measured in usual daily moves, the larger its fall over the next 1 day.
Consequence: A short taken on the close of a sharp bounce in a falling coin should be sized by the bounce's size and held for one day, since the giveback is spent after that.
Why:
- F1: The coin gives back part of the bounce on the next day only. On the 466 bounce bars in the regime, the coin's next-day return beat its normal daily drift by -0.58 % (t -2.28). Over days 2 to 5 it beat its drift by +0.20 % (t 0.36), and the plan's 5-day measure shows an unusual move of -0.10 % per case (strength -0.005, 376 cases).
- F2: The next-day giveback grows with the size of the bounce. Regressing the next-day return in usual daily moves on the bounce size gives a slope of -0.116 (t -2.55, 377 cases). The giveback is -0.71 % after a bounce of 2 to 2.5 usual moves, -1.16 % after 3 to 4 (t -1.96) and -2.33 % after more than 4 (t -2.35, 50 cases).
- F4: The book earns only on the first day of a position. Position gain is +0.158 % per bar on the first bar after entry (346 bars, sum +0.55). It is -0.237 % on the second bar (sum -0.82) and negative again from bar 6 onward (sum -0.60).
- F6: The 5-day move is smaller than the cost of a trade, but the next-day move is not. Over 5 days the unusual move per case is -0.10 % against a cost of 0.22 % (-0.4 times the cost). The next-day giveback is -0.58 % (about 2.6 times the cost) and -2.33 % after bounces above 4 usual moves.
