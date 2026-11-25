---
line: 7.g patterns
backtest: 049-02_wide-day-high-close-giveback_1d
idea tested: 049-02_wide-day-high-close-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4238 USD
---
## Findings
- **F1:** In agitated markets (the coin's 30-day swing above its median), the next day's excess return leans against today's return scaled by the 30-day swing: −0.61 % per unit, t −2.76 (day-clustered, 3,627 bars). In calm markets the slope is only −0.11 %, t −0.80 (3,622 bars). The slope is negative on all 6 coins (BTC t −2.94, ETH −3.01, XMR −3.54, ZEC −1.88, LTC −1.42, XRP −0.71) and in 11 of the 12 windows.
- **F2:** The agitated-market reversal is carried by falls. In the lowest decile of scaled daily return (mean −1.69 swings), the next day's excess is +1.90 %, t 2.65, 343 bars. Deciles 1 to 4 decline steadily (+0.48, +0.19, +0.16, +0.03 %). The highest decile (mean +1.88 swings) gives only −0.14 %, t −0.31. Over all markets, days below −2 swings are followed by +1.91 %, t 2.12, 166 bars.
- **F3:** On the close-location side, the brief's long half holds and the tested short half does not. Low close × width predicts the next day with slope +0.92 %, t 2.88 (7,321 bars). High close × width gives −0.30 %, t −1.23. Wide days closing in the lowest fifth of their range gain +1.23 % the next day, t 2.67, 426 bars, and that mean is positive in 11 of the 12 windows (w12 −0.02 %). Wide days closing in the top fifth give −0.27 %, t −0.78, 643 bars.
- **F4:** The book's gain came from its long side. Longs earned +0.031 % per bar over 3,977 bars, against −0.001 % on 4,179 short bars. In agitated markets longs earned +0.050 % per bar (1,747 bars), against +0.017 % in calm ones. The short side lost −0.017 % per bar in calm markets. Overall, the book's Sharpe was −0.29.
- **F5:** Within agitated down days, the close's place in the range adds little once the fall's size is known: slope −0.020, t −1.51, 1,795 bars. The size of the fall, more than the close location, carries the rebound.

## Ideas
- `049-02.g1_wide-day-low-close-rebound` (from F3, F4): The lower a coin closes in its day's high-low range, and the wider that day's range is against the coin's usual daily range over the past 30 days, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `049-02.g2_agitated-large-fall-next-day-rebound` (from F1, F2, F5): In an agitated market, the larger a coin's one-day fall against its usual daily move over the past 30 days, the larger its rise over the next day.
- `049-02.g3_agitated-daily-move-reversal` (from F1, F2): In an agitated market, the larger a coin's one-day move against its usual daily move over the past 30 days, the larger its move the opposite way over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
