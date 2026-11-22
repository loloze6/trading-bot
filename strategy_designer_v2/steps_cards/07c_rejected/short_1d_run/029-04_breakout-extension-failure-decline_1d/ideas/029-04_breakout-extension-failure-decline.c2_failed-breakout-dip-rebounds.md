---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline
line: 7.c rejected
backtest: 029-04_breakout-extension-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has closed above its prior 20-day closing high within the last 4 days and now closes back below that old high, it rises over the next 3 days, and the further its close sits below its highest close of the prior 20 days, the larger the rise.
Consequence: A deep slip back under a fresh breakout is a reason to buy the dip for a few days, not to short the failure.
Why:
- F4: Among failed breakouts, the further the close sat below its highest close of the prior 20 days, the higher the return that followed. The slope on that depth was −0.15 at 1 day (t −5.0, Spearman −0.12, p 0.00003, 1190 cases) and −0.39 at 3 days (t −5.5, Spearman −0.11, p 0.002, 766 cases). It faded at 5 and 10 days (Spearman p 0.39–0.40).
- F3: Failed breakouts were followed on average by a small rise, not a fall. The long-signed unusual move was +0.19 % at 5 days (t 0.52, 751 cases) and +0.94 % at 10 days (t 1.29, 578 cases). This was not stable across years: 2019 was −2.8 % (t −2.7, 83 cases) and 2020 was +2.5 % (t 3.2, 117 cases).
- F1: The test found the opposite of the idea. Higher peak excursions were followed by higher 5-day returns, not larger falls: slope +0.0027 per excursion point, t 3.3 over 751 non-overlapping cases. The positive slope held at every horizon: t 4.3 at 1 day (1402 cases), 4.3 at 3 days (908), 4.4 at 10 days (578) and 2.1 at 20 days (422).
