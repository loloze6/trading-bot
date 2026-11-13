---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-02_breakout-shock-continues
line: 7.g patterns
backtest: N3-02_breakout-shock-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A shock-up day closing at a new 21-day closing high is followed by a larger five-day rise when the coin's recent 20-day volatility is low or middling against its own past year, compared with when volatility is already high.
Consequence: A trader should take breakout-shock longs mainly when they come out of a calm market, and refuse them when volatility is already elevated.
Why:
- F3: Shock-up new highs depend on how volatile the coin has been. When the coin's 20-day volatility ranks in the lower two thirds of its past 250 bars, the 5-bar excess is +3.18% (t = 2.01, n = 69) and +2.76% (t = 2.21, n = 70). In the top third it is +0.89% (t = 0.51, n = 95). Across coins, five of six are positive in the calm cases.
- F4: The shock-up new-high effect is unstable by year: 2023 gives -1.69% (t = -2.65, n = 80) and 2022 gives -1.92% (t = -1.38, n = 56), while 2024 gives +2.06%. My own pooled recount of all shock-up new highs is +0.10% (t = 0.19, n = 527), against the verdict's t = 2.03, so the confirmed effect is fragile.
- F5: The book's trades split sharply by holding time. The 935 trades held one day or less lose on average (-1.87% net, median -1.35%). Trades held 1–2, 2–5 and 5–10 days gain +3.74%, +9.78% and +13.87% (n = 286, 224, 62). The 80 trades held over 10 days lose -7.52%. Most of the loss comes from breakouts that fail at once.
