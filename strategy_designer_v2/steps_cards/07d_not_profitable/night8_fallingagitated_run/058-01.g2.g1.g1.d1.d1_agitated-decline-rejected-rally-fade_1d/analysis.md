---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d
idea tested: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4080 USD
---
## Findings
- **F1:** The deepest fall of the book in folds B, C is -2.2 % and sits in w14. There 6 of the 8 worst short days came on one market-wide squeeze, with ETH, XMR, LTC and BTC all rising +11 % to +12 % the next day. One day held 4 coins' losses of more than 2 % of the book each. The other windows' deepest falls were only -0.3 % to -1.1 %. So the Calmar of 0.62, against the 0.75 needed, is set by clustered losses on one bad day, not by a weak mean.
- **F2:** The effect lives in the deepest sell-offs from the high. For cases whose close sits more than 0.51 of a usual daily move below the high (the deepest quarter), the next-day short-side move net of drift is +3.26 % (t 3.37, 72 cases on 41 days). In the middle two quarters it is +0.37 % (t 0.45, 72 cases) and +0.56 % (t 0.86, 72 cases).
- **F3:** The big losses do not fall in the deepest quarter. Of the 7 short days losing more than 2 %, 4 sit in the second quarter, where there is no effect, and 3 in the deepest; none sit in the two quarters nearest the high.
- **F4:** Trading only the deepest quarter makes a better book from fewer trades. In folds B, C, a book holding only those cases loses at most -1.27 %, against -2.16 % for all cases. It keeps 0.130 of the 0.170 summed gain on 41 days instead of 168, so its gain over its deepest fall is 10.2 against 7.9.
- **F5:** A deep sell-off from the high is not an effect of its own. In-profile days that are not first up days, with the close as far below the high, are followed by a rise: the short-side move is -1.22 % (t -2.46, 447 cases on 177 days). On up days that are not first up days it is +0.92 % (t 0.81, 51 cases). The effect needs the idea's own situation, the first up day sold off from its high.
- **F6:** The move shows mostly on the first day. For the deepest quarter, the short-side move net of drift is +3.26 % over 1 day (t 3.37), +2.99 % over 2 days (t 1.93) and +2.98 % over 3 days (t 1.61). Nothing more is added after day one, so a longer holding would only add risk.
- **F7:** The w14 squeeze losses came where the coin had already fallen 43 % to 63 % over 60 days, close to capitulation. In cases whose 60-day fall is deeper than 47 %, the move is +1.13 % (t 0.85, 54 cases). Elsewhere in the profile it is +1.89 % (t 3.21, 161 cases). Non-case days with that deep a fall show -0.67 % (t -0.86, 138 cases), so the deep fall is not an effect of its own. This is evidence, not proof.

## Ideas
- `058-01.g2.g1.g1.d1.d1.d1_deep-rejected-rally-fade` (from F2, F3, F4, F5, F6): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day only when the rally was sold off well below its high. The further that day's close sits below its high, measured against the standard deviation of its daily returns over the past 30 days, the larger that next-day fall, growing sharply for the deepest rejections.
- `058-01.g2.g1.g1.d1.d1.d2_rejected-rally-fade-before-capitulation` (from F1, F7, F2): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The further that day's close sits below its high, against the standard deviation of its daily returns over the past 30 days, the larger the fall, and the fall shrinks the deeper the coin's 60-day decline already is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
