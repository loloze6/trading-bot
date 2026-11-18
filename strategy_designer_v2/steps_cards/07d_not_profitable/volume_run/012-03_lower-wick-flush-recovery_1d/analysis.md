---
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
idea tested: 012-03_lower-wick-flush-recovery
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3072 USD
---
## Findings
- **F1:** The book loses because it sizes against its own edge: its position grows with the wick (mean allocation 0.80 in the top wick tercile against 0.11 in the bottom), but over 220 independent flush events the next-day return falls as the wick share rises (slope −0.073, t −2.51), and the 3-day slope is flat (t −0.22), so the correlation of position with next-day return is −0.20.
- **F2:** The flush rebound itself exists and is short: across 310 flush bars the mean next-day return is +1.19% (t 2.96), while by 5 days it is +0.11% (t 0.19). An equal-size long on the 220 independent events would have summed +0.56; the book's wick-sized position summed −0.51.
- **F3:** On a down bar the lower wick is the close's position in the bar's range (the wick and close-location regressions are identical), so a long wick means the close sat near the bar's high. Next-day return falls from +1.65% in the low-wick tercile to −0.50% in the high-wick tercile: the flushes that closed at their lows rebound most.
- **F4:** The rebound is carried by flushes that come after a 20-day decline: next-day return is +2.58% in the lowest 20-day-return tercile against −0.97% in the middle and +0.16% in the top (slope t −4.07 on 1 day, −2.11 on 3 days, 220 events). The book held less there (0.28) than in the other terciles (0.52, 0.48).
- **F5:** The rebound grows with the coin's prior 20-day volatility (slope on next-day return t 7.76, on 3-day return t 5.11, 220 events) and with the volume ratio (next-day t 2.67).
- **F6:** The book is in the market on about 3% of days, mean holding 1.09 bars. Mean daily return is −4.6e−6 against a daily standard deviation of 0.0036, giving Sharpe −0.03 and Calmar −0.02. Per-coin gain runs from +0.15 (XMR) to −0.14 (ZEC).

## Ideas
- `012-03_lower-wick-flush-recovery.d1_flush-closing-at-low-rebounds` (from F1, F2, F3): Among bars that fall sharply on a volume burst, the closer the close sits to the bar's low (the shorter the lower wick as a share of the bar's high-to-low range), the larger the price rise over the next 1 day.
- `012-03_lower-wick-flush-recovery.d2_flush-after-decline-rebounds` (from F2, F4): Among bars that fall sharply on a volume burst, the larger the rise over the next 1 day, the deeper the coin's 20-day return was negative before the bar.
- `012-03_lower-wick-flush-recovery.d3_volatile-flush-rebounds-harder` (from F2, F5): Among bars that fall sharply on a volume burst, the higher the coin's 20-day volatility of daily returns before the bar, the larger the price rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
