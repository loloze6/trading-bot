---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline
line: 7.c rejected
backtest: 029-04_breakout-extension-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 20-day closing high, reaches further above it within the next 3 days, and then closes back below the old high, the coin rises over the next day, and the larger the peak excursion above the old high was, the larger the rise.
Consequence: A large spike above the old high that slips back signals buyers still in control, a reason to refuse the short and lean long for the next day.
Why:
- F1: The test found the opposite of the idea. Higher peak excursions were followed by higher 5-day returns, not larger falls: slope +0.0027 per excursion point, t 3.3 over 751 non-overlapping cases. The positive slope held at every horizon: t 4.3 at 1 day (1402 cases), 4.3 at 3 days (908), 4.4 at 10 days (578) and 2.1 at 20 days (422).
- F2: The positive excursion slope is carried partly by its tail. At 5 days its rank correlation is only 0.019 (p 0.60), and the slope falls to t 1.7 once the excursion is cut at its 95th percentile. At 1 day the effect survives on ranks (Spearman 0.081, p 0.002, winsorised t 3.9), and at 10 days it is weaker (Spearman 0.083, p 0.046, winsorised t 2.5).
