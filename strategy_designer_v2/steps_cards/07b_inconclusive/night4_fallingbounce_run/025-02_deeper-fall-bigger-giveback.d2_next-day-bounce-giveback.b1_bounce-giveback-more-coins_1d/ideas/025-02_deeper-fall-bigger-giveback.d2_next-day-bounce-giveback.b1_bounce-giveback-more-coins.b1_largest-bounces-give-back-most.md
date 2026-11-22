---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise measured against the coin's usual daily move over the past 20 days, the larger its fall over the next day, with the largest rises giving back several times more than the moderate ones.
Consequence: A trader shorting bounces in falling coins should size by the raw bounce in usual daily moves and keep the trade for the largest bounces, where the next-day giveback is well above the cost of a trade.
Why:
- F1: The test's result is on the side the idea predicts but fails the grading check. On the 3,535 cases with forecast ≤ -2, the next-day unusual move in the short direction is +0.27 % (t 3.27). The larger-|forecast| half, however, trails the smaller half by -0.20 %, and across forecast quintiles the means show no order: +0.28 %, +0.40 %, +0.14 %, +0.12 %, +0.42 % (Spearman of |forecast| with the move 0.008).
- F2: The forecast's own shaping hides the grading the idea describes. Standardising over 60 bars and capping at 20 puts 29.5 % of cases at exactly -20. Also, 36 % of cases are days whose rise is below one usual daily move, so the median split mostly separates ordinary rises from ordinary rises.
- F3: Measured on the day's rise in usual daily moves itself, over all rising days in 90-day-falling coins, the next-day giveback grows with the rise. The mean move is +0.17 % for rises of 0 to 0.5 usual moves (n 3,361), +0.23 % for 1 to 1.5 (n 1,003), +0.45 % for 1.5 to 2 (n 447), +0.64 % for 2 to 3 (t 2.26, n 325) and +2.26 % above 3 (t 2.65, n 59). Rises above 2 usual moves minus rises of at most 1 give +0.73 % (Welch t 2.60, 384 vs 5,375 cases).
- F4: That grading holds across years but is weak at the median. The top quartile of rises minus the bottom quartile is positive in 7 of 8 years; 2021, at -1.23 %, is the exception. The simple vsr halves differ by only +0.15 % (Welch t 1.38), so the effect sits in the large rises.
- F7: The test already used every coin and every fold available, so more data cannot sharpen the answer. Per case, the total move (+0.19 %) is 0.8 times the 0.22 % cost of a trade. Rises above 2 usual moves (F3) give back +0.64 % to +2.26 % next day, about 3 to 10 times that cost.
