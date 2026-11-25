---
line: 7.g patterns
backtest: 047-01_falling-agitated-daily-fall-rebound_1d
idea tested: 047-01_falling-agitated-daily-fall-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5398 USD
---
## Findings
- **F1:** Inside the falling, agitated profile, the next-day excess return grows with the size of the day's fall. Falls beyond 2 usual moves give +2.67 % (t 1.79, 36 days), falls of 1 to 2 give +2.18 % (t 2.85, 79 days), 0.5 to 1 give +0.99 % (t 1.97) and 0 to 0.5 give +0.55 % (t 0.80). On all in-profile down days the slope is -1.20 % per usual move (t -3.21, 560 cases, 239 days). Outside the profile the same falls give only +0.63 % (t 1.13) and +0.46 % (t 1.44), with a slope of -0.14 (t -0.42).
- **F2:** Inside the profile, on up days the next-day fall depends on the day's high-to-low range rather than on the size of the rise. The range has a coefficient of -2.23 % per usual range (t -3.83, 542 cases, 225 days), holding the close-to-close rise at +1.62 (t 2.76). The rise alone has a slope of +0.20 (t 0.52), and up days have a flat mean of -1.05 % (t -1.97).
- **F3:** Inside the profile, down days in the widest third of their range (against the coin's usual range) are followed by +2.62 % (t 2.76, 189 cases, 81 days). The other two thirds give +0.65 % (t 0.95) and +0.83 % (t 1.70). In a joint regression the range (+0.95, t 1.12) and the fall (-0.66, t -0.97) cannot be told apart.
- **F4:** The rebound is spent in one day. On the second day after in-profile falls the excess return is -0.99 % (t -0.68) after falls beyond 2 usual moves and -0.10 % (t -0.16) after falls of 1 to 2. The 3-day return adds nothing beside the one-day move (-0.08, t -0.30).
- **F5:** Inside the profile, falls that close in the bottom fifth of the day's range rebound +2.22 % (t 2.59), and those closing in the top 40 % rebound +0.23 % (t 0.19). Close location adds nothing once the fall and the range are known (-0.18, t -0.08), and neither does the lower wick (+0.34, t 0.54).
- **F6:** The book's gain is concentrated. Its best 2 % of days carry 122 % of its mean daily gain. Windows w14, w16 and w18 (+0.11 %, +0.20 % and +0.09 % a day) are those where the coins sit in the profile 38 to 44 % of the time, against 0 to 23 % in most other windows.
- **F7:** Weekday splits are too thin to count. In-profile big falls on Saturday and Sunday give t 6.7 and 3.3, but on only 8 and 9 days. No other angle I looked at stood out.

## Ideas
- `047-01.g1_agitated-wide-up-day-next-day-fade` (from F2, F4): In a falling, agitated market, on a day a coin closes higher, the wider that day's high-to-low range against the coin's usual daily range, the larger its fall over the next day.
- `047-01.g2_agitated-wide-down-day-rebound` (from F3, F1, F4): In a falling, agitated market, on a day a coin closes lower, the wider that day's high-to-low range against the coin's usual daily range, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
