---
line: 7.g patterns
backtest: 032-02.b2.g1.d1_close-location-on-wide-days_1d
idea tested: 032-02.b2.g1.d1_close-location-on-wide-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3510 USD
---
## Findings
- **F1:** The low-close rebound is strongest when the coin is agitated: in the coin's top tercile of 20-day daily-return volatility, a close in the lowest fifth of the day's range is followed by a next-day excess return of +1.39 % (t 4.91, 511 cases), against -0.02 % (t -0.10, 470) in the lowest volatility tercile and +0.23 % (t 1.07, 508) in the middle one. On the same wide days the high-close side is weaker: -0.33 % (t -1.17, 502).
- **F2:** The tested idea's grading by range holds mostly on the long side. In the top tercile of range against its 20-day average, the lowest close fifth gains +1.10 % next day (t 4.80, 592) and the highest close fifth only -0.20 % (t -0.82, 608). In the bottom range tercile, every close fifth sits between -0.36 % and -0.10 % with no t beyond ±1.4. The book's gain per bar is 0.426 % on lowest-close-fifth bars against 0.026 % on highest-close-fifth bars.
- **F3:** A large one-day fall is followed by a rebound: the bottom fifth of one-day returns gains +0.71 % in excess the next day (t 4.56, 1722 cases). The other four fifths run from -0.05 % to -0.31 % (t +4.56 is the only positive t above 1), so the reversal sits in the down tail only.
- **F4:** In a coin that fell over its past 20 days (bottom tercile of 20-day return), a close near the day's high is followed by a fall that grows with the close location: next-day excess return goes from +0.59 % (t 2.47, 639) in the lowest close fifth to -0.41 % (t -1.39), -0.81 % (t -2.93, 420) and -1.16 % (t -3.76, 380) in the highest close fifth.
- **F5:** Over several days the short-term reversal turns into continuation. On a non-overlapping 3-day grid, the bottom fifth of 5-day returns loses a further -1.48 % in excess (t -3.05, 512 cases), while the top two fifths gain +0.67 % (t 2.05) and +0.74 % (t 1.66). On a 5-day grid the bottom fifth loses -1.52 % (t -1.97, 320).
- **F6:** The brief's own situation shows nothing. In a volatile decline (bottom 20-day-return tercile, top volatility tercile), the lowest fifth of 30-day range position gives +0.30 % next day (t 0.79, 430) and +1.50 % over 5 days (t 0.80, 81), which cannot be told from chance.
- **F7:** Weekday differences look sizeable (Thursday +0.47 %, t 3.19; Friday +0.39 %, t 2.87; Wednesday -0.49 %, t -2.69; 1231 to 1254 cases each). With seven groups among many angles and no theory behind them, I treat them as a lead, not grounds for an idea.

## Ideas
- `032-02.b2.g1.d1.g1_low-close-rebound-agitated-coins` (from F1, F2): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 1 day. The effect grows with how high the coin's 20-day volatility of daily returns stands against its own past levels.
- `032-02.b2.g1.d1.g2_rebound-after-outsized-down-day` (from F3): The larger a coin's one-day fall, measured against its usual daily move over the past 20 days, the more the coin rises over the next 1 day.
- `032-02.b2.g1.d1.g3_failed-bounce-in-downtrend` (from F4): In a coin that has fallen over its past 20 days, the higher the day's close sits within that day's high-low range, the more the coin falls over the next 1 day.
- `032-02.b2.g1.d1.g4_five-day-loss-continues` (from F5): The more a coin has fallen over its past 5 days, the more it keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
