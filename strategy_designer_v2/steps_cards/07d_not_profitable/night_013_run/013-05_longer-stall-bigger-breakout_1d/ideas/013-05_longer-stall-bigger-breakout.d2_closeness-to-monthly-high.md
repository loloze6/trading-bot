---
brief: 013_anchoring-to-recent-high
source-idea: 013-05_longer-stall-bigger-breakout
line: 7.d not profitable
backtest: 013-05_longer-stall-bigger-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close is to its prior 30-day closing high, and the further it sits above it, the larger the coin's return over the next 10 days.
Consequence: A trader would lean long in proportion to how near or how far above its 30-day high a coin closes, and stay away from coins far below that high.
Why:
- F3: The edge does not come from the stall count that grades the position. Raw stalls of 0–5 days give a mean 30-bar forward return of 64.1% (n = 45), but 15–30 days give −0.3% (n = 165) and 30–60 days give 10.1% (n = 130). The forecast's grading does not line up with what follows, yet it sizes the largest positions (allocation 1.20) on the longer stalls.
- F4: A close above a shorter recent high carries the same follow-through and happens far more often. 7.4% of bars close above their prior 30-day closing high, against 2.6% for the 365-day high. On a non-overlapping 10-bar grid the next-10-bar excess return is +5.39% above the 30-day high (n = 132, t = 2.59) and +4.16% above the 20-day high (n = 163, t = 2.36). In daily excess return it is +0.32% (t = 2.07) for the 30-day high and +0.73% (t = 2.93) for the 60-day high.
- F5: The follow-through is graded by closeness to the 60-day high, though not across the whole range. On the 10-bar grid, coins 20–30% below their 60-day high return −2.80% excess (t = −2.78), 5–10% below +0.30%, within 5% below +2.21% (t = 1.72) and above it +3.81% (t = 1.69). On the 30-day high, the bins from 5% to 30% below all return between −0.3% and −0.8%, against +5.4% above it.
