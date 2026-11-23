---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise, with the largest falls carrying almost all of the rebound.
Consequence: A trader buys only the large settlement falls and holds the rebound for a day, so that each trade captures several times its cost instead of paying a full cost on small falls that do not rebound.
Why:
- F1: The rebound is graded and only the largest settlement falls move enough to pay a trade. At 00:00 and 16:00 settlements, a 2-hour fall of 3 or more usual moves is followed by +0.43 % over 8 hours (1136 cases, strength 0.156). Falls of 1 to 1.5 usual moves give +0.21 %, and falls under 1 usual move give +0.02 % to −0.09 %. Against the 0.19 % cost of a trade, only the strongest falls carry the move.
- F2: The book spends half its trades on cases that carry no move. Cases with forecast 2–5 earn −0.001 % over 8 hours (3263 cases) and forecast 5–10 earn +0.04 % (3902 cases). Forecast 15–20 earns +0.24 % and the forecast-20 cases +0.28 % (2649 cases, mean fall −3.3 usual moves). Every case pays the same 0.19 % trade cost, which is why the mean daily return on days in a position stays at 0.011 %.
- F3: The rebound after a strong fall keeps growing past the 8 hours the book holds. At 00:00, falls of 3 or more usual moves give +0.62 % over 8 hours (t 2.66, 389 cases) and +1.44 % over 24 hours (t 4.30, total move +1.58 %). Across all 2584 falls of 2 or more usual moves at both settlements, the mean is about +0.32 % over 8 hours and +0.50 % over 24 hours, about 0.65 % total, or 3.4 times the trade's cost. The trades that stayed in longer (forecast-2–5 entries, held 21 hours on average) netted +0.29 % per trade. The forecast-15–20 entries, held 8.7 hours, netted only +0.08 %.
- F4: The settlement clock matters even with the fall itself as the condition. The same falls of 3 or more usual moves at 08:00 UTC, where no 00:00/16:00 settlement is tested, give +0.42 % over 8 hours (t 1.29) and +0.62 % over 24 hours. That is against +1.44 % over 24 hours after 00:00, so roughly half the 24-hour move belongs to the settlement situation. Across the day, falls of more than 1 usual move rebound most strongly after the 16:00 close (+0.34 % over 8 hours, t 6.06).
