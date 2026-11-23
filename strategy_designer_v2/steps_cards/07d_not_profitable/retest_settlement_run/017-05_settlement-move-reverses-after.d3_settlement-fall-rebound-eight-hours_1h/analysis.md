---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3951 USD
---
## Findings
- **F1:** The rebound is graded and only the largest settlement falls move enough to pay a trade. At 00:00 and 16:00 settlements, a 2-hour fall of 3 or more usual moves is followed by +0.43 % over 8 hours (1136 cases, strength 0.156). Falls of 1 to 1.5 usual moves give +0.21 %, and falls under 1 usual move give +0.02 % to −0.09 %. Against the 0.19 % cost of a trade, only the strongest falls carry the move.
- **F2:** The book spends half its trades on cases that carry no move. Cases with forecast 2–5 earn −0.001 % over 8 hours (3263 cases) and forecast 5–10 earn +0.04 % (3902 cases). Forecast 15–20 earns +0.24 % and the forecast-20 cases +0.28 % (2649 cases, mean fall −3.3 usual moves). Every case pays the same 0.19 % trade cost, which is why the mean daily return on days in a position stays at 0.011 %.
- **F3:** The rebound after a strong fall keeps growing past the 8 hours the book holds. At 00:00, falls of 3 or more usual moves give +0.62 % over 8 hours (t 2.66, 389 cases) and +1.44 % over 24 hours (t 4.30, total move +1.58 %). Across all 2584 falls of 2 or more usual moves at both settlements, the mean is about +0.32 % over 8 hours and +0.50 % over 24 hours, about 0.65 % total, or 3.4 times the trade's cost. The trades that stayed in longer (forecast-2–5 entries, held 21 hours on average) netted +0.29 % per trade. The forecast-15–20 entries, held 8.7 hours, netted only +0.08 %.
- **F4:** The settlement clock matters even with the fall itself as the condition. The same falls of 3 or more usual moves at 08:00 UTC, where no 00:00/16:00 settlement is tested, give +0.42 % over 8 hours (t 1.29) and +0.62 % over 24 hours. That is against +1.44 % over 24 hours after 00:00, so roughly half the 24-hour move belongs to the settlement situation. Across the day, falls of more than 1 usual move rebound most strongly after the 16:00 close (+0.34 % over 8 hours, t 6.06).
- **F5:** The book's losses concentrate in one year. Strong settlement falls (2 or more usual moves) lost −0.61 % over 8 hours and −1.08 % over 24 hours in 2022 (314 cases), and −0.22 % over 8 hours in 2025. In every other year they gained +0.19 % to +1.00 % over 8 hours. Cases inside a 7-day fall of 3–10 % lose −0.16 % over 8 hours (2678 cases), so the Calmar failure comes from these stretches. Every coin's strong falls are positive, from +0.14 % (BTC) to +0.61 % (XRP) over 8 hours.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound` (from F1, F2, F3, F4): The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise, with the largest falls carrying almost all of the rebound.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound` (from F4, F1): The return over the 8 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
