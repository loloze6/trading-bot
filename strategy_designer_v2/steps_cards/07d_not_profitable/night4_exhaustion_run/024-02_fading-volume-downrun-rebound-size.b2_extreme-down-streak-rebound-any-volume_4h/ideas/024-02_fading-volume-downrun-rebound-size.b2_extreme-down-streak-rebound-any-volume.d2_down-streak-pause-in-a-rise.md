---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods whose loss is several times its typical four-hour move over the past 30 days, it rises over the next one to three days, whatever the volume did during the streak, only while its 3-day return before the streak is a rise. The larger that prior 3-day rise, the larger the rebound.
Consequence: A trader buys sharp down-streaks that interrupt a fresh rise and refuses those inside a decline, cutting exposure during the coin's falls.
Why:
- F1: The book is the coin held with leverage near one, so its falls are the coin's falls. It holds a long position on 98.6 % of bars at a mean allocation of 0.98, and its daily returns correlate 0.93 with holding. Its deepest fall is −68.7 % against a yearly return of 29.6 % (Calmar 0.43), and its worst windows track the coin's: w14 −50.8 % against −49.4 %, w2 −36.9 % against −44.4 %, w7 −38.0 % against −49.8 %.
- F3: The idea has almost no size. Over 3 days its unusual move is +0.05 % per case (strength 0.007, t 0.48, 5,674 cases), against a trade cost of 0.19 %. Its total move of +0.46 % is mostly the coin's normal drift of +0.41 %.
- F5: The down streaks that rebound are pauses inside a rise. Cases whose 3-day return is in the top fifth (above +5.2 %) gain +1.02 % beyond drift (t 3.45, 1,104 cases), while the middle three fifths lose −0.35 % to −0.48 %. Combined with high volatility (F4), a prior 3-day rise gives +1.02 % (t 2.46, 560 cases).
