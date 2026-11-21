---
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3668 USD
---
## Findings
- **F1:** The book failed on its falls, not its gain: it earned 20.0 % a year against a deepest fall of 36.3 % (Calmar 0.55 against the 0.75 required), and its daily returns track holding the coins with a correlation of 0.92, because it holds a position on 92 % of bars.
- **F2:** Its three deepest falls (36.3 %, 35.5 % and 33.5 %) are the coins' own declines carried through. Holding the coins lost 59.7 % over the 2021 stretch (w12 to w16) and 59.2 % over the 2022 stretch (w1 to w10), and the book's worst windows are the coins' worst: w7 −0.20 against −0.58, w14 −0.20 against −0.52, w2 −0.18 against −0.46 in summed daily returns.
- **F3:** The grind measure barely grades what follows: the slope t is 0.91 on 4,191 cases, and the unusual move is +0.08 % per 48 hours, 0.011 of the usual 6.56 % move. That is 0.4 times the 0.19 % cost of a round trip, so most of the book's +0.35 % total move per case is the coins' drift.
- **F4:** The forecast's middle carries the effect, not its top. On 48-hour grid cases after a net fall, excess return is −24 bps in the lowest forecast quintile, +37 to +45 bps in quintiles 2 to 4, and only +5 bps in the most even (top) quintile. Flat cases run −14 bps against +21 bps for positive-forecast cases.
- **F5:** The rebound after a 24-hour fall lives in agitated markets, where the coin's 7-day hourly volatility is high against its 30-day volatility. In that upper tercile the 2-day excess return is +98 bps (126 bps total, 1,044 cases), against −11 bps in the calm tercile and −23 bps in the middle one. On all position bars, the top quintile of this ratio earns 1.34 bps per bar and carries 77 % of the book's whole gain; the other quintiles earn −0.00 to 0.23 bps.
- **F6:** Within the agitated tercile the grind grading is still positive (slope t 1.44), while in the calm tercile it turns negative (t −1.28). The grind measure adds something only when volatility has risen.
- **F7:** The rebound also concentrates after a deeper 7-day fall: the lowest 7-day-return tercile gives +56 bps excess over 2 days with slope t 1.45, against −27 bps for the middle tercile.
- **F8:** Exposure held in a mild 30-day decline (30-day return between −17 % and −4.5 %) loses money: −0.23 to −0.27 bps per position bar at a mean allocation of 0.51 to 0.55. Every other 30-day quintile earns +0.20 to +0.71 bps.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.d1_grind-rebound-in-agitation` (from F1, F2, F5, F6): The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days, only while its hourly moves over the last 7 days have been larger than over the last 30 days, and the more so the larger that ratio.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.d2_agitated-fall-rebound` (from F3, F5, F7): The more a coin's hourly volatility over the last 7 days exceeds its volatility over the last 30 days, the more it rises over the next 2 days after a fall over the last 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.d3_deep-volatile-week-rebound` (from F5, F7, F8): The deeper a coin's fall over the last 7 days, the more it rises over the next 2 days after a further fall over the last 24 hours, the more so the larger its last 7 days' hourly volatility against its last 30 days'.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
