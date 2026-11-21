---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the more evenly that rise was spread across its hourly steps (net 3-day move large relative to the sum of its absolute hourly moves), the more the coin keeps rising over the next 3 days.
Consequence: Favour longs after smooth, steady 3-day rises and size them by how smooth the rise was; refuse to chase rises made in a few violent hours.
Why:
- F2: Rises built as a grind continue: among 3-day rises, the tercile with the highest path efficiency (|72-bar net log move| over the sum of |hourly log moves|) is followed by +0.0084 excess 72-bar return (t 2.85, 955 non-overlapping cases), against −0.0039 (t −1.42) for the least efficient, most jumpy rises.
