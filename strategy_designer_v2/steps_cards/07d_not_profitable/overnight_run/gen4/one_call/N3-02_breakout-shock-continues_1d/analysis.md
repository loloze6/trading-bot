---
line: 7.d not profitable
backtest: N3-02_breakout-shock-continues_1d
idea tested: N3-02_breakout-shock-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3112 USD
---
## Findings
- **F1:** The book's information outlives its holding: 556 new-high signal cases taken at least 10 bars apart rise on average +0.40% over 1 bar (t 1.94), +1.46% over 5 bars (t 3.11) and +2.84% over 10 bars (t 3.65). With cases at least 20 bars apart, 373 cases rise +3.31% over 20 bars (t 2.34). Yet the median trade lasts 1 day, and the book is invested on only 27% of days.
- **F2:** Trades cut short lose and trades held longer win. The 935 trades closed within 1.5 days average −1.77% gross. The 286 trades of about 2 days make +3.84%, the 184 trades of 3–4 days make +9.06%, and the 94 trades of 5–9 days make +14.11%.
- **F3:** The exit is premature. In 51% of the cases the forecast is already 0 on the next bar. From that exit bar, the coin still rises +1.98% over the next 10 bars (t 2.19, 299 cases). The book sells the drift it was right about.
- **F4:** Fees are not the problem. Across 1590 long-only trades, gross gain averages +1.21% per trade (t 5.0) against 0.10% of fees. The shortfall is the book's daily return: 0.000364 against the coin's 0.00119, and a day-based Sharpe of 0.23 against the coin's 0.46.
- **F5:** A larger forecast does not earn more.
- **F6:** Losses concentrate in falling-market years. 10-bar returns after signals are −5.1% in 2018 (t −1.66, 41 cases) and −2.4% in 2022 (t −1.58, 62 cases). They are +6.2% in 2020, +6.2% in 2021 and +6.1% in 2024 (t 3.57, 2.14 and 2.81). The book's daily return is negative in 2022 and 2023.
- **F7:** The effect differs by coin. LTC's signals make −0.34% gross per trade and −0.3% over 10 bars (t −0.21), and XMR's make +0.7% over 10 bars (t 0.54). XRP and ZEC make +6.8% and +5.7% over 10 bars (t about 2.2).

## Ideas
- `N3-02_breakout-shock-continues.d1_breakout-drift-outlasts-the-high` (from F1, F2, F3, F4): After a coin closes at the highest close of its prior 20 days on an up day, its price keeps rising over the next ten or more days. The rise continues even when the following days close back below that new high.
- `N3-02_breakout-shock-continues.d2_the-high-not-the-shock` (from F5, F1): The size of the up day that makes the new 20-day closing high adds nothing. A new high made on an ordinary or small up day is followed by as large a rise over the next ten days as one made on an outsized day.
- `N3-02_breakout-shock-continues.d3_breakouts-pay-in-uptrends` (from F6, F1): The rise after a new 20-day closing high happens when the coin's close is above its own long average, for example its 200-day mean. When the close is below that average, the new high is followed by a fall over the next ten days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
