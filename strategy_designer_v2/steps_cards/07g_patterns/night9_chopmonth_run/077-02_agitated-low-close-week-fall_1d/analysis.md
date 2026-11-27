---
line: 7.g patterns
backtest: 077-02_agitated-low-close-week-fall_1d
idea tested: 077-02_agitated-low-close-week-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5902 USD
---
## Findings
- **F1:** The brief's week continuation in agitated markets depends on which 7-day grid is used, so it is not a pattern. On the grid that starts at each window's first bar, the slope of the 7-day unusual move on close location is +0.088 (day-clustered t 2.04, 648 cases, 166 days). Top-fifth closes gain +4.9 % (t 3.53) and bottom-fifth closes lose −4.3 % (t −2.58). On the six other grid offsets the slope runs from −0.085 (t −2.40) to +0.053 (t 1.19). The bottom-fifth 7-day move ranges from −8.0 % to +4.9 %, changing sign four times.
- **F2:** The tested short side, a low close followed by a 7-day fall, is not separable from zero. Its unusual move is +0.65 % per case (t 1.00, 1738 cases, 679 days), and after the coin's drift the total move is −0.36 %. That total is −1.6 times the 0.22 % cost of a trade. The book's Sharpe is −0.37 and it returns −13.3 % a year.
- **F3:** What close location does predict in agitated markets is the next day, and it reverses. The slope of the 1-day unusual move on close location is −0.019 (day-clustered t −3.05, 4487 cases, 1113 days). In calm markets it is −0.005 (t −1.30). The 2- and 3-day slopes are flat: −0.011 (t −0.92) and −0.006 (t −0.41).
- **F4:** That next-day reversal lives in the falling agitated profile.
- **F5:** In choppy agitated markets, the only empty cell on the map for shorts, top-fifth closes fall −3.3 % the next day (t −1.94, 25 days). The slope there is −0.062 (t −1.77, 87 days). After the many angles looked at, this does not stand out from chance.
- **F6:** Other angles hold nothing that is both new and strong. Agitated days with a fall beyond 2 of their 20-day swings rebound +3.9 % the next day (t 4.45, 77 cases, not clustered by day), which is the falling and agitated rebound family the map holds 16 times. Weekday effects (Wednesday −0.44 %, t −2.6; Friday +0.37 %, t 2.8) are not clustered by day across co-moving coins. Thirty-day trend buckets reach |t| 2.5 to 3.3 on only 58 to 104 cases, without day clustering.

## Ideas
- No ideas: The week continuation the brief claims flips sign with the choice of 7-day grid (F1), the only robust pattern is a next-day reversal the profile map already holds in falling agitated markets (F3, F4), and the one candidate in an empty cell, choppy agitated shorts, has a t under 2 on 25 days after many angles were looked at (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
