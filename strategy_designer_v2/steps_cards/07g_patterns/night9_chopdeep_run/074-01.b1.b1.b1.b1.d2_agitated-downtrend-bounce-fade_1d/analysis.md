---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.d2_agitated-downtrend-bounce-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4702 USD
---
## Findings
- **F1:** The tested idea's effect is concentrated in agitated falling markets and grows with the up day's width. On all up days in a falling agitated market, split into width terciles (range over its 20-day mean), the next-day unusual move is −0.17 % (t −0.28, 158 cases, 78 days), then −1.38 % (t −2.23, 156 cases, 83 days), then −2.35 % (t −2.84, 156 cases, 76 days). In falling calm markets the same terciles give only +0.40 %, +0.04 % and −0.49 % (t −1.27, 204 cases), so the fade is a feature of the agitated profile the map already holds (074-01 family).
- **F2:** The next-day fall after a wide up day in a falling market is partly given back on the second day. After up days at least 1.3 times as wide as their 20-day mean, in a falling market, the next day's unusual move is −1.98 % (t −3.01, 165 cases, 76 days). The day after that moves +1.13 % (t 2.21, 164 cases, 75 days). Over the two days together it nets −0.83 % (t −1.13). The tested idea does not describe this second-day rebound.
- **F3:** A similar fade appears in choppy agitated markets, a profile whose short side the map shows empty (0 strategies). On up days in a choppy agitated market, the next-day unusual move is −0.42 % in the narrowest width tercile (t −0.96, 49 cases), −1.59 % in the middle tercile (t −2.12, 50 cases, 43 days) and −1.78 % in the widest (t −1.39, 50 cases, 41 days). In choppy calm markets the terciles give +0.15 %, −0.06 % and −0.20 %, all with |t| < 0.4, so there the pattern is absent. Each agitated tercile is small and was found among many angles, so it is near the edge of chance.
- **F4:** Wide up days do not fade in rising markets. Over all trends, next-day weakness grows with an up day's width only in falling markets (Spearman of width vs next-day return −0.14) and barely in choppy ones (−0.06), not in rising ones (+0.03). Wide high-closing up days in a rising market are followed by +0.72 % (t 1.35, 297 cases), and the widest tercile of rising calm up days by +0.64 % (t 1.20).
- **F5:** The book's profit rests on a few coins, and the newer coins in the test lose. Over 101 trades, net trade results average +1.38 %, with a median of +2.20 % and a standard deviation of 6.34 %. ETH (+43.2 % summed over 22 trades) and XRP (+41.7 % over 11) carry the gain. ADA (−31.3 % over 7), DOGE (−12.5 %, 1 trade) and TRX (−6.4 %, 1 trade) lose. The book is in a position on 3 % of coin-days, which is why the Calmar falls short (0.71) even though trades are about 5 times their cost.

## Ideas
- `074-01.b1.b1.b1.b1.d2.g1_falling-wide-bounce-second-day-rebound` (from F2, F1): In a falling market, after an up day whose high-to-low range is wide against the coin's average daily range over the past 20 days, the coin rises on the second day after it, once the next day's fade is over. The wider that up day's range, the larger the second day's rise.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.b1.b1.b1.b1.d2.g2_choppy-agitated-wide-rally-fade` (from F3, F4): In a choppy, agitated market, an up day whose high-to-low range is wide against the coin's average daily range over the past 20 days is followed by a fall over the next day. The wider that day's range, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
