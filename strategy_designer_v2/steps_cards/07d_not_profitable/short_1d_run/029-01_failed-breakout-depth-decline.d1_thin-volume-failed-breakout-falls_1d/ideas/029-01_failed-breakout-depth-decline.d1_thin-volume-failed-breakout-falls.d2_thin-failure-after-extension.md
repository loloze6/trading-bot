---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days. The thinner the breakout day's volume against its 20-day average, and the larger the coin's 20-day rise into the breakout, the larger that fall.
Consequence: A trader would size a short on a failed breakout by both how thin the breakout volume was and how extended the run into it was, keeping full size for thin failures at the end of large rises.
Why:
- F1: The move per case cannot cover a trade. The total short-side move is +0.10 % over 5 days, against a cost of 0.19 % per trade, because the coins' normal drift runs −0.59 % against the short. The 394 actual trades lost −1.84 % gross on average (t −4.26), with only 30 % winners, so the mean daily return was 5.2e-05 against the 0.0005 required.
- F2: The forecast does not keep the idea's grading. 442 of its 468 non-zero bars sit at exactly −20, so the book is short at full size whether the breakout volume was a little thin or very thin. It is also in the market only 2–9 % of bars per coin.
- F3: Across all 498 failed breakouts rebuilt from prices, only the thinnest quartile shows a fall. That quartile, with a mean thinness of 0.38 (volume about 38 % below its 20-day average), has a short-side unusual move of +1.15 % (t 1.42, 125 cases). The heavy-volume failures move −0.99 % (t −1.59, 303 cases). The near-average quartile (thinness 0.05) moves −1.09 %.
- F7: The book does better when the breakout came after a larger 20-day rise. Trade losses shrink steadily from −3.51 % (t −3.79) in the lowest 20-day-return quartile (+1 %) to −1.27 % (t −1.13) in the highest (+40 %). The failed-breakout cases in that highest quartile are the only 20-day quartile with a positive short-side unusual move (+0.41 %).
