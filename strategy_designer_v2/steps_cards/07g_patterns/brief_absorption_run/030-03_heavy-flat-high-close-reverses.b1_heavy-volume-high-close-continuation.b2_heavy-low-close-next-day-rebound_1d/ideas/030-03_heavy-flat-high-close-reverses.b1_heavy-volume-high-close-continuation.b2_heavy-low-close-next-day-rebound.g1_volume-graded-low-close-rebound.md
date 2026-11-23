---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is above its 20-day average, the closer its close sits to the day's low, the more the coin rises over the next 1 day. The heavier that day's volume relative to its 20-day average, the stronger this rebound.
Consequence: Scale a one-day rebound bet on a low close by how heavy the day's volume was, instead of switching it on at one volume level.
Why:
- F1: The next-day rebound after a low close grows with volume, not only above the tested 2x cut. The slope of the next-day excess return on close location (0 at the high, 1 at the low) is 0.04 % at t 0.20 for volume under 0.7x its 20-day mean (n 5644). It is 0.97 % at t 1.82 for 1.5–2x (n 1223), 1.74 % at t 2.78 for 2–3x (n 846) and 4.38 % at t 3.18 above 3x (n 446). A close in the bottom fifth of the range on volume above 3x is followed by +3.64 % (n 63).
- F5: The heavy-volume low-close effect is a one-day effect. On a non-overlapping 3-day grid its slope falls to 2.67 % at t 1.54 (n 447), and 2.71 % at t 1.21 once the day's return is controlled. For down moves in general, the 2-day reversal holds at t -2.85 (n 7498) and the 3-day at t -1.94 (n 4859).
