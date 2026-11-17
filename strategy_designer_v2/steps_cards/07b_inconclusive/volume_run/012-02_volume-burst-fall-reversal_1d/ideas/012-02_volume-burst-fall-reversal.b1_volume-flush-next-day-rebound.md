---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.b inconclusive
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day.
Consequence: A trader buying a high-volume flush should expect the retrace mainly within the next day and not count on it lasting to three days.
Why:
- F1: The volume-ratio effect shows at 1 day and fades after: on the same 440-odd thinned sharp-fall cases, the slope of excess return on volume ratio is +0.00715 with t 3.61 (n 443) over 1 day, then +0.00432 with t 1.59 (n 440) over 3 days, -0.0028 with t -0.79 (n 434) over 5 days, and -0.0025 with t -0.54 (n 421) over 10 days.
- F2: The highest-volume falls rebound on the next day and give it back afterward: the top volume-ratio tercile (mean ratio 3.58, n 148) has a mean excess return of +1.14% over 1 day, -0.25% over 3 days (which is why the supporting check failed) and -1.78% over 5 days, against -0.04%, -0.82% and -1.31% for the lowest tercile.
