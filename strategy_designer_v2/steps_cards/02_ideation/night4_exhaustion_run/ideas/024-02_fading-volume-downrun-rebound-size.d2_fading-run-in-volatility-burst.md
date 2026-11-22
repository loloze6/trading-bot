---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days. The rise is larger the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, and the higher the coin's volatility over the past 5 days against its volatility over the past 30 days.
Consequence: A trader takes the rebound bet when the down-run comes in a burst of unusually high recent volatility and refuses it in quiet markets, where the cases lose.
Why:
- F7: The rebound also grows with recent volatility against its usual level. Splitting cases by the ratio of 5-day to 30-day volatility of 4h returns, the lowest quartile has an unusual move of −0.51 % (t −2.09, 852 cases) and the highest +0.69 % (t 2.14, 851 cases).
- F8: The forecast's size is graded as the idea says. Its top tier (17.7–20, 2,289 cases) has an unusual move of +0.52 % (t 2.88) and its lowest tier (2–9.9, 1,145 cases) −0.63 % (t −2.92), so the losses come from the weaker streaks.
- F3: The tested effect is absent overall: over 4,578 cases the unusual 18-bar move is about 0.00 % (step 5: t 0.002, strength 0.000), and the +0.41 % total move is only the coin's normal drift.
