---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-02_breakout-shock-continues
line: 7.d not profitable
backtest: N3-02_breakout-shock-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes at the highest close of its prior 20 days on an up day, its price keeps rising over the next ten or more days. The rise continues even when the following days close back below that new high.
Consequence: A trader who buys a new 20-day closing high should keep the position for the following one to two weeks rather than selling on the first day without a new high.
Why:
- F1: The book's information outlives its holding: 556 new-high signal cases taken at least 10 bars apart rise on average +0.40% over 1 bar (t 1.94), +1.46% over 5 bars (t 3.11) and +2.84% over 10 bars (t 3.65). With cases at least 20 bars apart, 373 cases rise +3.31% over 20 bars (t 2.34). Yet the median trade lasts 1 day, and the book is invested on only 27% of days.
- F2: Trades cut short lose and trades held longer win. The 935 trades closed within 1.5 days average −1.77% gross. The 286 trades of about 2 days make +3.84%, the 184 trades of 3–4 days make +9.06%, and the 94 trades of 5–9 days make +14.11%.
- F3: The exit is premature. In 51% of the cases the forecast is already 0 on the next bar. From that exit bar, the coin still rises +1.98% over the next 10 bars (t 2.19, 299 cases). The book sells the drift it was right about.
- F4: Fees are not the problem. Across 1590 long-only trades, gross gain averages +1.21% per trade (t 5.0) against 0.10% of fees. The shortfall is the book's daily return: 0.000364 against the coin's 0.00119, and a day-based Sharpe of 0.23 against the coin's 0.46.
