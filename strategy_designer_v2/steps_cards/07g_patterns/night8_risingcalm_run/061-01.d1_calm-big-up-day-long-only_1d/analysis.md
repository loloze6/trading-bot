---
line: 7.g patterns
backtest: 061-01.d1_calm-big-up-day-long-only_1d
idea tested: 061-01.d1_calm-big-up-day-long-only
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5720 USD
---
## Findings
- **F1:** The tested long-only book earns the coins' drift and nothing more: its unusual move per case is +0.01 % (t 0.02, 822 days, 1765 cases) against a total move of +0.64 %. In folds B and C the calm 5-day excess return after up days is about 0 for days of 0.3 to 1 swing (+0.28 %, t 0.34, 141 cases). Only the rare large days carry anything: 1 to 2 swings give +2.3 % (t 1.94, 76 cases) and over 2 swings give +6.8 % (t 2.07, 28 cases). Most cases are small days with no move, which is why the size is 0 while the slope's t is 3.5.
- **F2:** In a falling calm market (60-day return below −10 %, calm profile), the 5-day return measured in swing units (5-day return over the 30-day daily standard deviation times √5) is followed by a graded continuation over the next 5 days. The excess returns by bin, with t clustered by day, are:
- **F3:** The F2 continuation of falls does not appear in agitated markets; there it turns to a rebound. In a falling agitated market, a 5-day fall below −0.5 swing units is followed by +1.3 % (t 0.31, 46 cases) and below −1.5 by +8.7 % (t 1.02, 9 cases). In calm markets as a whole, a 5-day move of −1.5 to −0.5 swings is followed by −2.4 % (t −2.95, 129 cases), against +1.3 % (t 1.14, 141 cases) in agitated markets.
- **F4:** The calm continuation of falls in F2 holds on 5 of the 6 coins, with excess t near −2 on ETH, LTC, XMR and ZEC (−5.9 %, −4.8 %, −6.7 %, −5.0 %), weaker on BTC (−4.5 %, t −1.22) and flat on XRP (−1.2 %, t −0.39). It is concentrated in 2018 (−6.1 %, t −2.11, 46 cases) and 2019 (−5.0 %, t −1.45). 2020 and 2021 hold only 12 cases and do not show it.
- **F5:** In calm markets, the coin's 3-day return in swing units predicts its next 5 days better than the single day does. The pooled date-clustered slope t is 3.17 for the 3-day return against 2.81 for the 1-day. On the down side alone the 3-day slope's t is 2.64 while the 1-day down-day slope's t is 0.34. The 3-day slope stays positive at 3 days (t 2.03) and 10 days (t 2.26). In agitated markets every one of these slopes has a t between −1.0 and +0.6.
- **F6:** The book's strongest weekday pattern is Friday and Saturday: the book earns +0.27 % (t 3.83) and +0.28 % (t 3.42) on those days, and the coins earn +0.53 % (t 3.66) and +0.57 % (t 4.09). It is largest in rising calm markets (+1.41 %, t 2.80, 248 cases). The map already holds this as 045-01 (rising market late-week gain), so it is not a discovery.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.d1.g1_falling-calm-decline-continues` (from F2, F3, F4): In a falling, calm market, the larger a coin's fall over the last 5 days against the standard deviation of its daily returns over the past 30 days, the larger its further fall over the next 5 days.
- `061-01.d1.g2_calm-three-day-move-continues` (from F5, F1, F3): In a calm market, the larger a coin's 3-day return against the standard deviation of its daily returns over the past 30 days, the larger its move the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
