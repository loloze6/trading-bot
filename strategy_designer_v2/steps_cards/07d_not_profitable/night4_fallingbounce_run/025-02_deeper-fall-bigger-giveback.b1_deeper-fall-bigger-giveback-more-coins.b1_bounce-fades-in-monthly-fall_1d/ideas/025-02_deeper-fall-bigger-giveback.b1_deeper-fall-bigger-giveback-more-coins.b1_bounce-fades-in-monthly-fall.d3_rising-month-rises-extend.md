---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, the larger its one-day rise measured in its usual daily moves, the larger its further rise over the next 3 days.
Consequence: A trader would go long after sharp rises in coins up over the past month, taking a larger long the larger the rise, and would refuse to short those rises.
Why:
- F1: The book barely trades and so barely earns: only 227 of 36768 bars (0.6 %) were active, the book was non-zero on 305 of 2898 days, and its mean daily return is 0.004 % against 0.138 % for holding the coins, so the 0.71 % per-case edge never adds up to a daily return.
- F6: The opposite holds in rising months. On up days with a positive 30-day return, larger rises are followed by larger further rises: the 3-day slope is +1.44 % per usual move (corr +0.105, p < 0.0001, 2476 cases). With both the 90-day and 30-day returns positive, rises of 2 to 3 usual moves are followed by +0.76 % the next day (t 2.68, n 543) and +1.32 % over 3 days (t 1.94, 191 cases).
- F7: At 1 day, the per-case moves of the broader situations (-0.34 % to -0.81 %) are only 1.5 to 3.7 times the 0.22 % cost of a trade. At 3 days, the same situations give -1.4 % to -5.0 %, 6 to 22 times the cost.
