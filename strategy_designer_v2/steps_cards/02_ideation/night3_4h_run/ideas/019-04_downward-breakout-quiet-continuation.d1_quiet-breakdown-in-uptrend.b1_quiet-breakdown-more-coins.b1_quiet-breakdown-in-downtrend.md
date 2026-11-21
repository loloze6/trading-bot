---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is negative.
Consequence: Short a downward break out of a narrow range in a coin that has fallen over the past month, sized up as the range is narrower, and treat the same break in a rising month as no reason to short.
Why:
- F1: The tested shorts sit where the effect is zero. In rising months, the 18-bar cases the forecast actually traded (forecast at or below -2, the narrow stretches only) earned a short-side unusual move of +0.01 % (t 0.04, 813 cases) and +0.56 % over 36 bars (t 1.16, 630 cases). Step 5 measured -0.39 % (t -0.94, 1107 cases), so the result is zero to the wrong side, not a weak real effect.
- F4: In falling months (30-day return at or below 0), the tested narrowness grading does show, along its own gradient. By width quintile, narrowest to widest, the 18-bar short-side unusual move is +1.13 % (t 3.35, 588 cases), +0.77 % (t 2.52), +0.03 %, +0.25 % and -0.46 % (t -1.19). Over all 2,938 cases the Spearman between width and the move is -0.079 (p < 0.0001); at 36 bars it is weaker (narrowest quintile +1.50 %, t 2.37; rho -0.030, p 0.19).
- F5: The falling-month narrow-break effect is broad but not uniform, and it fails in the steepest falls.
- F6: Both moves are large next to the cost of a trade (0.22 % for a buy and a sell). The falling-month narrowest-quintile short has a total move of +0.60 % (2.7 times the cost) and an unusual move of +1.13 % (5 times). The rising-month widest-quintile break, read as a long, has a total move of +2.22 % (10 times) and an unusual move of +1.69 % (7.7 times). By F11, both are in the size range where books have paid.
