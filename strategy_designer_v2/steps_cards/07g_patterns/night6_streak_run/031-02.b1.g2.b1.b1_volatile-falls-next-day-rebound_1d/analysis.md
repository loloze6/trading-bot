---
line: 7.g patterns
backtest: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound_1d
idea tested: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5815 USD
---
## Findings
- **F1:** Across the 19 coins, the latest day's volume against its own 30-day average (log volume minus its 30-day mean) predicts the next day's excess return: slope +0.0033 per log unit, day-clustered t 3.01 over 33748 cases on 2682 days. The top fifth of volume surprises is followed by +0.43 % (t 2.63, 1861 days) and the bottom two fifths by -0.20 % and -0.22 % (t -1.57 and -2.20). It is the strongest pattern in roughly fifteen angles examined, which covered streaks, z-returns, close location, range, weekday, volatility rank and positions.
- **F2:** The volume effect is concentrated on down days: slope +0.0045 (t 2.64, 2225 days) against +0.0023 on up days (t 1.86). Down days in the top fifth of volume surprise are followed by +0.75 % excess the next day (t 3.07, 1087 days), against +0.14 % (t 0.75) for up days in that fifth. That is about 3.4 times the 0.22 % cost of a trade, while the tested idea's unusual move was +0.06 % (t 0.45).
- **F3:** The volume effect is broad and not just a wide-range day in disguise. Its slope is positive in 18 of 19 coins, with BTC the exception at -0.00003 (t -0.02), and positive in 7 of 8 years, though only 2024 has t above 2 (2.80). Removing the day's range relative to its 60-day average, which correlates 0.64 with volume surprise, still leaves a slope of +0.0023 (t 2.08). It also shows over 3 days on a non-overlapping grid: slope +0.0062, t 1.98, 962 days.
- **F4:** The day's range relative to its 60-day average sorts the next day too, but less clearly than volume:
- **F5:** The brief's streak question shows nothing beyond chance. The next-day excess return by streak length from -5 to +5 has no grading, and only two isolated cells pass |t| = 2: a 3-day down streak at +0.67 % (t 2.10) and a single up day at -0.24 % (t -2.00). The next day after a standardised daily return sorted into deciles is also flat: slope t -1.17.
- **F6:** The book mostly moves with the coins: the correlation of its daily return with the coins' is 0.72. Its 20 worst days average -10.96 % against -12.91 % for the coins, and its 20 best days +9.18 % against +14.46 %. It takes most of the market's crashes and less of its rallies, which fits a Calmar of 0.43.

## Ideas
- `031-02.b1.g2.b1.b1.g1_heavy-volume-falls-rebound-next-day` (from F2, F1, F3): The more a coin's volume on a down day exceeds its own average volume of the past 30 days, the more the coin rises over the next 1 day.
- `031-02.b1.g2.b1.b1.g2_volume-surprise-predicts-drift` (from F1, F3): The higher a coin's latest-day volume relative to its own average volume of the past 30 days, the higher its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
