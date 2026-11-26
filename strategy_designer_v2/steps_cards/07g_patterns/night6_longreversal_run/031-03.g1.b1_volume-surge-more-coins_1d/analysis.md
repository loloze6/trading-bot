---
line: 7.g patterns
backtest: 031-03.g1.b1_volume-surge-more-coins_1d
idea tested: 031-03.g1.b1_volume-surge-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6683 USD
---
## Findings
- **F1:** The volume ratio (14-day over 30-day mean volume, minus 1), signed by the direction of the coin's 14-day return, sorts the next 14 days' excess return measured in that direction, on the 14-day grid. The bottom quintile shows −4.48 % (t −2.80, 306 cases, 87 days) and the top quintile +6.41 % (t 2.85, 306 cases, 93 days), rising across the quintiles (−1.58 %, +0.97 %, +0.87 %). These per-case moves are about ten times the tested idea's +0.66 % unusual move and well above the 0.22 % cost of a trade.
- **F2:** The volume ratio's own sign carries about twice the edge after a 14-day rise as after a 14-day fall: +4.04 % per case (t 2.72, 763 cases, 105 days) against +1.88 % (t 1.80, 767 cases, 109 days). After a rise, the excess 14-day return climbs with the volume-ratio quartile: −4.43 % (t −2.42), −0.45 %, +1.07 %, +6.47 % (t 1.83). So a rise that comes with swelling volume carries on, and a rise on drying volume gives back.
- **F3:** After a 14-day fall, only drying volume shows a clear lean: the lowest volume-ratio quartile is followed by −4.41 % excess (t −2.16, 63 days), while the highest is only +1.90 % (t 0.79). Drying volume is followed by weakness whichever way price moved before.
- **F4:** The F1 effect sits in the later years (2022 onward): top quintile +8.47 % (t 3.05, 53 days), bottom −5.43 % (t −2.80, 48 days). The earlier years (2018–2021) show +1.70 % (t 0.49) and −2.66 % (t −0.95), so the pattern is not uniform across eras.
- **F5:** The tested book earns almost entirely on its long side, which is why it fails to beat holding:
- **F6:** Other angles I looked at showed nothing that stands out once day-clustered:

## Ideas
- `031-03.g1.b1.g1_volume-confirmed-two-week-continuation` (from F1, F2, F3, F4): The more a coin's mean daily volume over the last 14 days has risen above its 30-day mean while its 14-day return points one way, the further its price moves that same way over the next 14 days; the more that volume has dried up below its 30-day mean, the more its price moves against its 14-day return over the next 14 days.
- `031-03.g1.b1.g2_swelling-volume-after-rises` (from F2, F5): When a coin has risen over the last 14 days, the more its mean daily volume over those 14 days has risen above its 30-day mean, the more its price rises over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
