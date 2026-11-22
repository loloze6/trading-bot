---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 5-day volatility is high relative to its 30-day volatility and its last 3 days were a rise, a sharp four-hour down-streak is followed by a rise over the next three days. The higher the volatility ratio and the larger the 3-day rise, the larger the rise that follows.
Consequence: A trader takes only dips inside a volatile rally, which in these cases moved about five times the cost of a trade beyond drift.
Why:
- F4: The rebound appears only while the coin's 5-day volatility is high against its 30-day volatility. In the top fifth of that ratio (1.20 to 2.36), cases rise +1.05 % beyond drift (t 3.20, 847 cases). In the bottom fifth (0.21 to 0.67), they fall −0.50 % (t −2.08, 847 cases). On long bars the same split gives +0.093 % against −0.004 % per 4-hour bar.
- F5: The down streaks that rebound are pauses inside a rise. Cases whose 3-day return is in the top fifth (above +5.2 %) gain +1.02 % beyond drift (t 3.45, 1,104 cases), while the middle three fifths lose −0.35 % to −0.48 %. Combined with high volatility (F4), a prior 3-day rise gives +1.02 % (t 2.46, 560 cases).
- F3: The idea has almost no size. Over 3 days its unusual move is +0.05 % per case (strength 0.007, t 0.48, 5,674 cases), against a trade cost of 0.19 %. Its total move of +0.46 % is mostly the coin's normal drift of +0.41 %.
