---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days, only while its hourly moves over the last 7 days have been larger than over the last 30 days, and the more so the larger that ratio.
Consequence: A trader would buy a grinding daily decline only once the coin's recent volatility has risen above its monthly norm, and stay out of the same decline in a calm market, where it carries no rebound and only adds the coin's falls to the book.
Why:
- F1: The book failed on its falls, not its gain: it earned 20.0 % a year against a deepest fall of 36.3 % (Calmar 0.55 against the 0.75 required), and its daily returns track holding the coins with a correlation of 0.92, because it holds a position on 92 % of bars.
- F2: Its three deepest falls (36.3 %, 35.5 % and 33.5 %) are the coins' own declines carried through. Holding the coins lost 59.7 % over the 2021 stretch (w12 to w16) and 59.2 % over the 2022 stretch (w1 to w10), and the book's worst windows are the coins' worst: w7 −0.20 against −0.58, w14 −0.20 against −0.52, w2 −0.18 against −0.46 in summed daily returns.
- F5: The rebound after a 24-hour fall lives in agitated markets, where the coin's 7-day hourly volatility is high against its 30-day volatility. In that upper tercile the 2-day excess return is +98 bps (126 bps total, 1,044 cases), against −11 bps in the calm tercile and −23 bps in the middle one. On all position bars, the top quintile of this ratio earns 1.34 bps per bar and carries 77 % of the book's whole gain; the other quintiles earn −0.00 to 0.23 bps.
- F6: Within the agitated tercile the grind grading is still positive (slope t 1.44), while in the calm tercile it turns negative (t −1.28). The grind measure adds something only when volatility has risen.
