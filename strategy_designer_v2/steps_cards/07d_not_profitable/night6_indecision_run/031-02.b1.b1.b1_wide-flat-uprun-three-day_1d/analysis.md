---
line: 7.d confirmed, not profitable
backtest: 031-02.b1.b1.b1_wide-flat-uprun-three-day_1d
idea tested: 031-02.b1.b1.b1_wide-flat-uprun-three-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4393 USD
---
## Findings
- **F1:** The book failed only on trading too rarely, at 0.0085 trades per day against the 0.01 rule; the strict signal (range at least 1.5x the 20-day mean, body at most 10 % of range, up over 6 days) fired 169 times on 129 days, only 0.0045 cases per coin-day across 37,254 coin-days (323 trades in all).
- **F2:** Relaxing only the flatness to a body of at most 30 % of the range, with the same width and the same up-run, keeps the effect while tripling the cases: 546 cases on 325 days (0.0147 per coin-day), unusual 3-day move +1.90 % (t 3.08), strength 0.21, total move +2.41 %, which is 11 times the 0.22 % cost of a trade.
- **F3:** Flatness grades the move inside wide up-run days. At range ratio 0.667 or below, the unusual move is +3.63 % (t 3.56) for a body of at most 10 %, +2.52 % (t 3.26) at most 20 %, +1.90 % (t 3.08) at most 30 % and +1.27 % (t 2.95, 1514 cases) for a body over 40 % of the range.
- **F4:** Range width grades the move among up-run days with a body of at most 30 %. The 20-day mean range over the day's range gives +2.46 % at 0.5 or below (198 cases), +1.02 % at 0.5–0.667 (261), +0.57 % at 0.667–0.85 (393) and about −0.2 % to −0.45 % above 0.85 (narrow days); the slope of the move on width is +0.00105.
- **F5:** In the broad case the prior rise grades the move. By quartile of the standardised 6-day rise the move is −0.61 %, +1.69 %, +3.42 % and +3.73 % (128–129 cases each), with a slope of +0.0101 per unit of standardised rise.
- **F6:** The added breadth is not an effect of its own, because the up-run (the idea's own situation) is what carries it. Wide days with a body of at most 30 % and no 6-day rise earn +0.00 % over 3 days (302 cases, t 0.00), and narrow flat days inside up-runs earn −0.23 % (999 cases, t −0.72).
- **F7:** The 3-day horizon is the right one, since the broad case over 5 days earns +1.26 % with t 1.84 (322 days), weaker than over 3 days. The broad case is positive in 6 of 8 years, negative in 2018 (−5.6 %, 10 cases) and 2022 (−1.6 %, 53 cases).

## Ideas
- `031-02.b1.b1.b1.d1_small-body-wide-uprun-day` (from F1, F2, F3, F5, F6, F7): After a coin has risen over the past 5 days, a day whose range is wide compared with its average daily range over the past 20 days and whose body is small against that range is followed by a further rise over the next 3 days; the smaller the body against the range and the larger the 5-day rise, the larger the further rise.
- `031-02.b1.b1.b1.d2_width-graded-flat-uprun-day` (from F1, F4, F5, F6, F7): After a coin has risen over the past 5 days, a day whose close lands near its open is followed by a further rise over the next 3 days; the wider that day's range against its average daily range over the past 20 days, and the larger the 5-day rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
