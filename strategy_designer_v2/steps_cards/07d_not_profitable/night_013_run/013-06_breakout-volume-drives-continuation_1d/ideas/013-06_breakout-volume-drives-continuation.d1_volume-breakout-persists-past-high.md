---
brief: 013_anchoring-to-recent-high
source-idea: 013-06_breakout-volume-drives-continuation
line: 7.d not profitable
backtest: 013-06_breakout-volume-drives-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 30 days. That return keeps accruing through the days after the close slips back below the new high.
Consequence: A trader should hold a high-volume breakout for the full 30 days, sized by the breakout-day volume ratio, rather than only while the coin keeps printing new highs.
Why:
- F1: The book is almost never in the market: the "close above the prior 365-close high" regime is active on only 2.59% of bars (in position on 2.56%), so the mean daily return is 0.000153 against a required 0.0005, even though active days average +0.40%.
- F2: The regime switches off at once because it needs a fresh new high every day. The 209 active runs last 2.12 bars on average (median 2), and 93 of them last a single bar, so the book exits long before the 30-day horizon the idea forecasts.
- F3: The gain the book leaves behind is large. Over 30 days from the breakout, the book made a mean +5.1% against the coin's +12.1% (59 non-overlapping cases), and after a run ends the coin still rises a mean +7.9% over the next 30 days (t 2.57, n 146 runs, median +1.1%).
- F4: The follow-through is graded by breakout-day volume and keeps building past 30 days. Over the next 30 days, high-volume-tercile breakouts returned +30.7%, mid +5.9% and low −0.1%. Over 60 days the figures were +53.3%, +1.1% and −1.6%. The book captured only +8.4%, +5.0% and +1.5% of those 30-day moves.
- F6: Breakouts carry deep interim dips: the mean worst point within the 30 days is −13.7%, and the close sits below the breakout price on 48% of those days. Because the book's exposure is tied to day-by-day new highs, it is out of the market for the recovery from these dips.
