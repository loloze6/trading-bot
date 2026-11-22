---
line: 7.g patterns
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
idea tested: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3697 USD
---
## Findings
- **F1:** The two hours from 21:00 to 23:00 UTC (the close of the bar starting at 20:00 to the close of the bar starting at 22:00) end above the coin's normal 2-hour drift by +0.073 % for BTC (t 4.09) and +0.095 % for ETH (t 4.10), over 2917 non-overlapping days each. In the all-bar hourly table, hour 20 (+0.045 %, t 4.00) and hour 21 (+0.040 %, t 3.69) are the only two of 24 hours above t 3.
- **F2:** The 21:00–23:00 UTC rise holds across the sample: it is positive in 7 of 8 years (2019 to 2021 and 2023 to 2025 each have t ≥ 2.2; only 2022 is negative, at −0.063 %, t −1.44) and on all 7 weekdays (+0.068 % to +0.107 %).
- **F3:** The 21:00–23:00 UTC rise is graded by the size of the day's move since 00:00 UTC, in either direction: it is +0.155 % (t 3.42) after the most negative fifth of days so far and +0.121 % (t 3.30) after the most positive fifth, against +0.014 % to +0.069 % for the three middle fifths (1167 days each).
- **F4:** The idea's own situation does not show up without its trend condition: hours falling 2.5 to 4 typical moves on volume 0.67 to 1.5 times average are followed by −0.048 % unusual 6-hour moves (t −0.26, 178 cases). The brief's high-volume continuation is absent too: large falls on more than 3 times average volume are followed by +0.239 % (t 0.64, 164 cases), the opposite of continuation.
- **F5:** Weakness in hours 0 to 2 UTC is significant overall (hour 2: −0.032 %, t −3.35) but has not lasted: it is −0.074 % (t −3.35) in 2018 and −0.042 % (t −2.53) in 2022, but +0.001 % in 2024 and +0.013 % in 2025.
- **F6:** Momentum over 7 days is weak and not monotone. The 6-hour unusual move after a 7-day return above 10 % is +0.095 % (t 2.54, 3344 cases), and the top fifth of 7-day returns gives +0.243 % over 24 hours (t 1.89). But the correlation of the 7-day return with the 24-hour unusual move is −0.001 for both coins, and the top fifth is negative in 2018 and 2022.
- **F7:** The book's gains are uneven by weekday and by entry time. Daily book returns are +0.179 % on Saturday (t 3.46) and +0.168 % on Friday (t 2.55), but negative on Thursday (−0.058 %) and Sunday (−0.062 %). Trades entered in the 4-hour blocks from 00:00, 12:00 and 16:00 UTC have net t of 2.89, 2.96 and 3.76, while those entered from 04:00 to 12:00 UTC are negative.

## Ideas
- `028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers.g1_late-utc-evening-rise` (from F1, F2, F3): Each coin rises more than its normal drift over the two hours from 21:00 to 23:00 UTC. The larger the coin's move since 00:00 UTC that day, up or down, the larger that evening rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
