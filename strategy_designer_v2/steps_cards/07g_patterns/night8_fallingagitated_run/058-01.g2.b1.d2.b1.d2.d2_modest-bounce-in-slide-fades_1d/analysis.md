---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4554 USD
---
## Findings
- **F1:** Inside the falling-agitated profile, the tested idea's whole gain sits in its deepest slides: on its active bars, the deepest quarter of prior four-day falls (four-day scaled return below −1.49) is followed by a next-day unusual move of −3.93 % on the long side (t_day −2.47, 76 cases), while the other three quarters give −0.88 %, −0.54 % and +0.69 % (t_day −0.97, −0.69, +0.70).
- **F2:** The same holds for every in-profile up day, not only those of at most one swing: after the deepest quarter of four-day falls (below −1.12 swings) the next day's unusual move is −2.23 % (t_day −2.15, 159 cases on 76 days), against +0.19 % and −0.14 % in the two middle quarters.
- **F3:** The fade of an up day after a deep slide also shows in falling calm markets, a separate sample outside the tested profile: there, the deepest quarter of four-day falls (below −1.68 swings) is followed by −1.48 % the next day (t_day −2.14, 165 cases on 79 days), against −0.36 %, +0.33 % and +0.61 % in the other quarters. In choppy and rising markets the deepest quarter gives −0.37 % (t_day −0.80, 377 cases), so the effect is tied to a falling trend, not to agitation.
- **F4:** In-profile up days of up to one swing fade by themselves (−0.95 % after 0 to 0.5 swings, t_day −1.85; −1.17 % after 0.5 to 1 swing, t_day −1.75), while up days above one swing do not (−0.17 % and +0.21 %). This matches the tested idea's cap on the size of the up day.
- **F5:** The strongest in-profile patterns are the long-side rebounds: down days after the deepest quarter of four-day falls gain +3.36 % the next day (t_day 2.96, 165 cases on 80 days), and closes in the lowest fifth of the day's range gain +1.95 % (t_day 2.49, 281 cases). Both repeat rebound ideas the map already holds in falling agitated long (038-01, 047-01, 051-01, 045-01, 039-02), so they are not discoveries.
- **F6:** The book's profit rests on a few days: its daily returns have a skew of 7.27, its 10 best days carry 101 % of its summed daily returns, and window w14 alone carries 0.108 of the 0.254 total. This is consistent with a gain concentrated in the rare deep-slide cases (F1) and with the Calmar failure.
- **F7:** Read across about 70 groupings, the other angles show nothing that stands out: weekday (in-profile Tuesday +1.25 %, t_day 1.60), day's range quartile (top quartile +1.24 %, t_day 1.60), an up day after a four-day rise (−1.22 %, t_day −2.04, not graded across the quarters), and the three-day horizon by three-day move (|t_day| ≤ 1.44).

## Ideas
- `058-01.g2.b1.d2.b1.d2.d2.g1_deep-slide-bounce-fades` (from F1, F2, F4, F6): In a falling, agitated market, an up day of up to about one usual swing that follows a four-day fall is given back over the next day, and the give-back grows faster than the depth of the fall against the coin's 30-day swing: shallow slides give back almost nothing, the deepest give back most.
- `058-01.g2.b1.d2.b1.d2.d2.g2_calm-slide-bounce-fades` (from F3, F2): In a falling, calm market, an up day that follows a four-day fall is given back over the next day, more the deeper that four-day fall against the coin's 30-day swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
