---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The lower a coin's hourly volatility over the past 3 days stands against its hourly volatility over the past 30 days while it has fallen over those 3 days, the more the coin keeps falling over the next 3 days.
Consequence: A quiet decline is a reason to stay short or avoid buying, and a decline made in turbulent hours is a reason to refuse the short.
Why:
- F4: Falls continue only when they are quiet: among active grid bars, those whose 3-day hourly volatility over 30-day hourly volatility was lowest (ratio 0.57 and 0.79) were followed by excess 72-bar returns of -0.0070 (t -1.98, n 509) and -0.0074 (t -2.24, n 509), and those with the highest ratio (1.01 and 1.48) by +0.0024 and +0.0048; the graded Spearman of the ratio against excess return is 0.07 (t 2.14, n 2035).
- F5: Inside quiet falls both grind halves continued (-0.0088 for the lower half of the grind measure and -0.0053 for the upper half, n about 520 each), while in turbulent falls both were flat or reversed (+0.0001 and +0.0068), so the volatility state carries the effect and grind share adds little to it.
- F6: Small falls continued and large falls reversed: the smallest 3-day falls (mean -0.8 %) were followed by -0.0098 excess, and the largest (mean -13.2 %) by +0.0041 (n about 667 each); falls inside a strong 30-day rise (mean +34 %) were followed by +0.0040 (t 1.02, n 509).
- F7: Being short in turbulent hours lost money on a bar level: on short bars in the top volatility-ratio quarter the daily-scaled gross was -0.0017, against +0.0007 in the calmest quarter.
