---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin's 3-day fall came from choppy hours, with much hourly movement in both directions for little net decline, the further the coin falls over the next 3 days.
Consequence: A trader would refuse to buy a choppy 3-day decline and would treat its choppiness as a sign the selling is not finished.
Why:
- F7: Falls built from choppy hours (lowest net-fall-to-total-hourly-movement quintile) kept falling, with excess -0.0087 (t -2.39, n=534), while the middle quintile rose +0.0035.
- F3: Even before fees there is almost nothing to harvest: the forecast was positive on every active bar (no short side), and the strongest bucket (forecast above 5, n=1898 fallen grid cases) had a mean excess 72-bar return of -0.0031 (t -1.69), the opposite sign to the idea.
