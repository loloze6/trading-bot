---
line: 7.d confirmed, not profitable
backtest: 033-02_close-near-high-gives-back_1d
idea tested: 033-02_close-near-high-gives-back
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3809 USD
---
## Findings
- **F1:** The book is short on every bar, and the coins' rise and the fees outweigh its timing. Its mean position is -0.43 of the book. It is -0.71 at closes in the top fifth of the range and still -0.09 in the bottom fifth, and it holds a position on 100 % of the coins' days. Its gain from the market's own rise is -0.059 % a day against a total gain before fees of -0.011 % a day, so timing adds +0.048 % a day. Fees take a further 0.025 % a bar on a turnover of 0.26 a bar. The result is a Sharpe of -0.62 and a Calmar of -0.28.
- **F2:** The losses come from rising markets. With the 60-day return above +10 %, closes at or above 0.8 of the range are followed by a next day +0.46 % above the coin's mean (t 1.66, 454 cases). The book loses 0.56 % a day on those bars and 0.29 % a day over all rising bars (1652). By year, the book's gain per bar is +0.18 % in 2018, when coins fell, against -0.14 % in 2020 and -0.11 % in 2021, when they rose.
- **F3:** In a falling, agitated market the give-back is large. There, closes at or above 0.8 of the range are followed by a next day -1.08 % below the coin's mean (t -2.69, 158 cases), and the book earns +0.81 % a day on them. The condition alone does not carry the move: falling, agitated bars without a high close are followed by +0.28 % (t 1.23, 647). This fits the theory: late chasing buyers in a falling, agitated market pay up against the trend, so their premium is the most fragile. In a falling, calm market high closes give +0.15 % (t 0.43), so agitation is what matters.
- **F4:** After a 20-day fall of more than 10 %, closes in the top fifth of the range are followed by -1.04 % against the coin's mean (t -3.46, 402 cases), where the book earned +0.57 % a bar. After a 20-day rise, the top fifth gives -0.03 % (t -0.11, 651). On the 60-day trend the condition alone does not carry the move: falling bars without a high close give -0.09 % (t -0.76, 1679), against -0.36 % for falling bars with a high close (t -1.36, 384).
- **F5:** The effect is graded, and too small on average to pay for a trade, but its strong cases are not.
- **F6:** The give-back lasts one day only. The two-day return after a top-fifth close is +0.24 %, against -0.20 % for the next day alone. A longer holding would not repair the book; choosing which cases to trade would.

## Ideas
- `033-02.d1_high-close-fades-in-selloffs` (from F1, F2, F3, F5): In a falling, agitated market, the nearer a coin's daily close sits to that day's high, measured as its position within the day's high-low range, the larger the fall in its price over the next day.
- `033-02.d2_high-close-fades-after-declines` (from F1, F2, F4, F6): When a coin's 20-day return is a fall, the nearer its daily close sits to that day's high, measured as its position within the day's high-low range, the larger the fall in its price over the next day.
- `033-02.d3_wide-day-high-close-gives-back` (from F1, F5, F6): The nearer a coin's daily close sits to the high of a day whose high-low range is at least as wide as its recent usual range, measured as the close's position within that range, the larger the fall in its price over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
