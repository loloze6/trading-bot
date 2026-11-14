---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's past 10-day return lands in its top fifth, or after a daily rise of two to three standard deviations, price keeps rising over the next 10 days more than after ordinary days, also while the 50-day SMA is below the 200-day SMA.
Consequence: A trader would go long, or close shorts, after a large up-move rather than fade it.
Why:
- F6: Up-moves continue rather than reverse. After the top quintile of past-10-bar returns (>+10.4%), the forward 10-bar return is +4.78% (t 2.48) in the flat state and +2.80% (t 2.44, 57% up) in the short state. After daily moves of +2 to +3 sigma, the forward 10-bar return is +4.94%, against +1.25% after moves within ±1 sigma.
- F9: Leverage magnifies the book's losses. On short bars the allocation reaches −2.2 (5% quantile −1.72, mean −0.85), and the book's daily return is almost exactly allocation × coin return (corr 0.99999). This gives daily book tails of −58% (worst) and −14.9% (1% quantile). The worst 1% of book days coincide with a +11.6% coin day at a mean allocation of −1.56.
