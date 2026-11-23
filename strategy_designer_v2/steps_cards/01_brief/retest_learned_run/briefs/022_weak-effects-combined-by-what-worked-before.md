---
bar: 1d
---
Many known effects in crypto prices are real but weak on their own: momentum over weeks, short reversals after large days, nearness to recent highs, and the level of volatility. Combined, with each effect weighted by how well it predicted returns over the past, they forecast the coming days better than any one of them alone, because their errors are partly unrelated.

The reason is mine, from forecasting practice. Each effect captures a different behaviour of traders (trend following, overreaction, anchoring, risk aversion), so their mistakes do not all happen at the same time. A combination learned only from data already known at each date, and relearned as time goes on, keeps the weights that have recently worked and lowers those that have stopped working.

Because the combination is meant to be stronger than each effect, its move over the coming days should be larger next to the cost of a trade than that of any single effect.

The theory is wrong if the learned combination predicts no better than the best single effect on dates it was not learned on, or if its weights change so much from one period to the next that what it learned does not carry forward.
