---
line: 7.g patterns
backtest: 041-02_wide-down-day-next-day-rebound_1d
idea tested: 041-02_wide-down-day-next-day-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5775 USD
---
## Findings
- **F1:** The tested rebound sits almost entirely in the widest down days: next-day excess return by range quintile (range in 30-day swing units, per coin) is +0.30 %, -0.17 %, +0.12 %, +0.14 % for quintiles 1 to 4 (all t_day under 1.1) and +1.14 % for the widest fifth (797 cases on 252 days, t_day 2.61), which is about 6 times the 0.19 % cost of a trade, against +0.17 % for the idea's average case.
- **F2:** With cases on the same day counted together, the linear slope of next-day excess return on range over down days is weaker than step 5's pooled t of 5.8: coefficient +0.0039, t_day 1.86 on 3520 cases. With the day's return in swing units, close location and volume added, range keeps its coefficient (+0.0037) but falls to t_day 1.03, so the effect is convex: concentrated in the widest days rather than spread along the scale.
- **F3:** On all days together, the next day moves against the day's direction in proportion to its range: next-day excess return on range × sign of the day's return has coefficient -0.0023, t_day -2.93, over 7177 cases. On the day's signed return in swing units it is -0.0030, t_day -2.20, so range carries the reversal better than the return's size.
- **F4:** Up days reverse by range only when the trend is falling. In a falling 60-day trend, next-day excess return on the up day's range has slope -0.0067, t_day -2.42, over 974 cases. In a choppy trend the slope is -0.0012 (t -0.36), and in a rising trend +0.0016 (t +0.86). Up days in falling and choppy trends are followed by -0.58 % (t_day -1.77) and -0.61 % (t_day -1.89), against +0.34 % in rising trends.
- **F5:** On up days, holding the day's gain fixed, a wider range predicts a lower next day: range coefficient -0.0053 (t_day -2.34), return +0.0058 (t_day +2.27), over 3657 cases; with close location and volume added, -0.0074 (t_day -2.62). An up day whose range is large next to its gain gives back. On its own, the up day's range has no slope (t -0.84).
- **F6:** The down-day rebound is unevenly spread over time. Among the two widest range quintiles of down days, windows w18 (+3.70 %, t 4.99) and w10 (+1.53 %, t 5.93) carry it, while w9, w15 and w16 are negative (-0.50 %, -0.30 %, -0.88 %). By coin all six are positive, from +0.45 % (LTC) to +1.03 % (XRP).
- **F7:** The book is mostly the market's own move. Its daily returns correlate 0.68 with the coins' mean daily return; on its worst 2 % of days the coins fell 11.3 % on average, and on its best 2 % they rose 9.4 %.
- **F8:** Several other angles show nothing that stands out once same-day cases are taken together. On down days, volume adds nothing beside range (log volume ratio t_day 0.36 in the joint fit, 2.02 alone, overlapping with range). Close location on down days is weak (t_day -1.17 jointly). No weekday has |t_day| above 1.2. These angles add no idea.

## Ideas
- `041-02.g1_extreme-range-down-day-rebound` (from F1, F2, F6): After a down-closing day, a coin rises over the next day, and the rise grows faster than in proportion as that day's high-to-low range widens beyond its usual width in units of its 30-day daily-return swing, so that the widest days carry most of the move back.
- `041-02.g2_falling-market-wide-rally-fades` (from F4, F3): In a falling market, after an up-closing day, a coin falls over the next day, more so the wider that day's high-to-low range in units of its 30-day daily-return swing.
- `041-02.g3_symmetric-wide-range-next-day-reversal` (from F3, F1, F5): After any day, a coin moves against that day's direction over the next day, more so the wider that day's high-to-low range in units of its 30-day daily-return swing.
- `041-02.g4_wide-swing-small-gain-up-fade` (from F5, F4): After an up-closing day, a coin falls over the next day, more so the wider that day's high-to-low range is next to its close-to-close gain, both in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
