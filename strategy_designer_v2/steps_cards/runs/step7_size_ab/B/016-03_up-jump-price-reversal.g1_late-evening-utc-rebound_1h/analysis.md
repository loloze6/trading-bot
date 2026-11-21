---
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4046 USD
---
## Findings
- **F1:** The book loses because each trade earns less than it costs. Its 11,085 trades, held a median of 120 minutes, earn a mean of +7.6 bps before fees (t 4.4) against about 10 bps of commission recorded per trade. The net mean is -2.4 bps per trade and the book's mean daily return is -0.026 %. Only BTC (+4.7 bps) and ETH (+3.4 bps) are net positive per trade. The idea's own size says the same: its 2-hour total move per case is +0.14 % against 0.21 % for a buy and a sell, which is 0.6 times the cost.
- **F2:** The same 24-hour fall pays over days, at every hour of the day. On a non-overlapping 24-hour grid, the deepest fifth of 24-hour falls is followed over the next 24 hours by +45 bps above the coin's drift (+58 bps total). That is a strength of 0.090, with t 4.4 on 3,417 cases and t 3.9 against the middle fifth. Over the next 72 hours it is followed by +81 bps above drift (+114 bps total), a strength of 0.094, with t 2.9 on 1,102 cases. The 72-hour excess is positive in all 6 coins (+26 to +167 bps) and in 71 % of the windows, so its total move is about 5 times the 21 bps round trip.
- **F3:** The rebound after a 24-hour fall is not special to the 20:00 UTC close. The rank correlation of the past 24-hour return with the next 2-hour return is negative at 22 of 24 hours (-0.009 to -0.099). The 19:00 bar is only the strongest of them (-0.099), so the evening-only window drops most of the cases without picking out a distinct effect.
- **F4:** Inside the tested 2-hour window the effect is not graded at its extreme. The top fifth of positive forecasts gives +6.8 bps of 2-hour excess, against +17.7 bps for the fourth fifth. Over 8 hours the top fifth gives -16.5 bps against +13.0 bps for the fourth fifth. This forecast is the fall standardised against only its last 60 hourly values, and on the daily horizon the payoff is concentrated in the deepest fifth of raw 24-hour falls (F2: +45 bps, while the second fifth shows -10.8 bps).
- **F5:** Over 3 days, the strongest 7-day rises keep going. Over the next 72 hours, the top fifth of 7-day returns is followed by +73 bps above drift (+107 bps total), a strength of 0.081. That excess is positive in 5 of 6 coins and in 62.5 % of the windows. It is the weakest of these findings: the fifths below the top are flat to negative, and no t was computed for this group.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound` (from F1, F2, F3, F4): The more a coin has fallen over its last 24 hours, the more it rises over the next 3 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound` (from F1, F2, F3): The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running` (from F5): The more a coin has risen over its last 7 days, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
