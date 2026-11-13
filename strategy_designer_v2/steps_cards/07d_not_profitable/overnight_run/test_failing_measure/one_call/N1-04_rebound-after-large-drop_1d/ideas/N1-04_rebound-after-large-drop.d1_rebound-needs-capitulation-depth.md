---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.d not profitable
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin rebounds the next day after a down day when that day comes on top of a deep fall already under way, its close more than about a fifth below its 50-day average or more than a tenth below its close of five days earlier. When the fall is only moderate, the next day keeps drifting lower.
Consequence: Take the rebound long only after a drop that deepens an already large decline, and refuse it during moderate declines, where the book takes losses on the crash days that set its drawdown.
Why:
- F1: The book fails only on Calmar (0.748 against 0.75); its pooled daily equity falls 46.2% at its deepest. The deepest falls inside windows are w9 (-40.5%), w13 (-36.2%), w14 (-32.9%), w2 (-32.3%) and w3 (-32.2%). In each of these the coins themselves fell 44% to 68%.
- F2: The book's falls come from crash days that hit every coin at once. On the book's 30 worst days its daily return averaged -13.8%, against -9.8% for the coins' mean. On those days 98.9% of the coin-days the book held lost money.
- F4: Where the drop happens relative to the 50-day average decides whether it pays:
- F5: The prior five days tell the same story. After a five-day fall of more than 10%, active bars earn 0.92% above the coin's mean (t 3.66, n=889). After a shallow five-day fall of 0% to 3%, they earn -0.22% (t -2.29, n=1324).
