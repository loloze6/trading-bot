---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline
line: 7.d not profitable
backtest: 029-02_breakout-volume-trapped-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close above the prior 20-day high is followed within 3 days by a close back below that high, the coin falls over the next 5 days, and the smaller the coin's 20-day return before the breakout, the larger the fall.
Consequence: A trader would short failed breakouts out of flat ranges and refuse those that come after a strong run-up, where the failure is only a pause.
Why:
- F1: The book loses because after failed breakouts the coins rose. Over 385 first-in-cell short bets, the short's unusual 5-day move is -0.47 % (t -0.71) and its total move is -1.04 %, with a hit rate of 0.49. Step 5 finds -0.77 % unusual and -1.36 % total over 335 cases. The book is short (mean allocation -0.82) on 10.3 % of days, and on those days the coin gains +0.236 % a day while the book loses -0.203 % a day.
- F2: The grading by breakout volume runs the wrong way. Cases with forecast size 12.2 to 20 (288 cases) lose -1.02 % unusual (t -1.32), while the 97 smaller ones gain +1.17 % (t 0.88). Step 5's slope is -0.0015, and the correlation of forecast size with the unusual move is -0.07.
- F3: The short pays only where the coin had not already run up before the break. In the lowest quartile of 20-day return (below about +7.6 %), the unusual move is +2.03 % (t 2.35, 80 cases, total +1.46 %), about 10 times the 0.19 % trade cost. The middle two quartiles lose -3.06 % (t -1.50) and -1.86 % (t -1.85).
- F6: The loss is concentrated in strong up years. The result is positive in 2018 (+5.25 %, t 2.07) and 2019 (+4.29 %, t 2.11) and negative in 2020 (-2.24 %, t -2.05), 2024 (-1.54 %) and 2025 (-3.65 %). The book's daily loss splits into -0.0098 % from the coins' rise and -0.0126 % from timing.
