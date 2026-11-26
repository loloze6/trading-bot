---
line: 7.d confirmed, not profitable
backtest: 049-01_wide-day-low-close-rebound_1d
idea tested: 049-01_wide-day-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4136 USD
---
## Findings
- **F1:** The tested book fails on its falls because it is long almost all the time. Its forecast is never negative and is standardised over its own past 60 values, so it averages 8.6 and the book holds a position on 98 % of coin-days, with a mean allocation of 0.37. As a result the book's daily returns correlate 0.81 with holding the coins (beta 0.35), and its deepest fall, 42 % from peak, came in w14, a window where holding lost 52 %.
- **F2:** The bottom three fifths of the forecast carry no effect, yet the book holds them. Their next-day excess returns are −0.31 % (t −2.3), −0.14 % (t −1.2) and −0.58 % (t −4.2), against +0.35 % (t 2.6) and +0.68 % (t 4.8) in the top two fifths, with about 1,740 bars per fifth. Holding the top 40 % only, on folds B and C before fees, raises Calmar from 1.51 to 2.06 and Sharpe from 1.34 to 1.64, and cuts the w14 loss from −21 % to −7 %.
- **F3:** The 30 worst book days followed bars with a mean forecast of 19.2 and a mean position of 0.84, where the average is 8.6 and 0.37. On those bars the coin's 20-day return averaged −8.2 % (average +2.1 %) and its 10-day against 60-day swing averaged 1.20 (average 0.91). The book's losses come from full-size longs taken after wide low closes inside falls.
- **F4:** The effect lives in a rising market. With the coin's 60-day return above +10 %, a wide-day low close (some width above usual) is followed by a next-day excess return of +0.85 % (t 3.7, 782 bars). In falling markets the same close gives −0.01 % (t −0.05, 601 bars), and in choppy markets −0.10 % (t −0.3, 261 bars). A rising trend without the signal earns −0.08 % (t −0.5, 870 bars), so the trend is not an effect of its own. It fits the theory: in an uptrend, buyers stand ready to absorb a forced sell-off, while in a falling market the forced flow continues.
- **F5:** The information sits in the part of the range beyond the coin's usual width. The product depth × max(range multiple − 1, 0) is zero on 4,684 bars, which show −0.17 % excess (t −2.3). Among its positive values the top quarter gives +0.78 % (t 3.3, 641 bars), against +0.15 % to +0.33 % in the lower three quarters.
- **F6:** A book on that excess-width product, on folds B and C before fees, sits in a position on 29 % of coin-days. Its deepest fall is 13 %, against 38 % for the tested book, and its Calmar is 1.21. It keeps most of the timing but gives up the market's drift.
- **F7:** The opposite side does not hold, so a short side would lose. Wide days that close near their high are followed by positive excess returns in three of four strength quarters: +0.37 %, +0.83 % (t 3.6) and +0.39 %. Only the strongest quarter is negative, at −0.21 % (t −0.8).

## Ideas
- `049-01.d1_rising-market-wide-day-low-close-rebound` (from F1, F3, F4): In a rising market, the lower a coin closes in its day's high-low range, and the wider that day's range is against the coin's usual daily range over the past 30 days, the larger its rise over the next day.
- `049-01.d2_excess-width-low-close-rebound` (from F2, F5, F6): The lower a coin closes in its day's high-low range, and the more that day's range exceeds the coin's usual daily range over the past 30 days, the larger its rise over the next day.
- `049-01.d3_rising-market-excess-width-rebound` (from F2, F3, F4, F5): In a rising market, the lower a coin closes in its day's high-low range, and the more that day's range exceeds the coin's usual daily range over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
