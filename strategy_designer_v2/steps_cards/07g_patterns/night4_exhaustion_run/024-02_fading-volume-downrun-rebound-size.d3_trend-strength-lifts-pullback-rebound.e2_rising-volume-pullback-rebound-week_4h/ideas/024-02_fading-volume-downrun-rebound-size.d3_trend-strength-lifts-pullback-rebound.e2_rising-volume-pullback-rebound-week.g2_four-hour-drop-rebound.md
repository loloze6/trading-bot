---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin falls over a four-hour period, it rises over the next four hours. The larger the fall relative to the coin's usual four-hour move over the past 30 days, the larger the rise.
Consequence: A trader can buy a coin after a sharp four-hour drop, sized by how unusual the drop was, for a four-hour rebound, and refuse to sell into such drops.
Why:
- F3: The next 4h bar reverses the last one, and more so the larger the fall. Grouped by the last bar's return over the coin's 30-day bar volatility, the next bar returns +16.7 bp after z ≤ -2 (2,641 bars, t 2.43), +11.4 bp after -2 to -1 (7,874, t 4.11), +3.6 bp after -1 to 0 (37,230, t 3.77) and -2.0 bp after 0 to 1 (37,722, t -2.17). After rises above +1 the next bar is not significant: +0.1 bp, t 0.05; +6.9 bp, t 1.23.
