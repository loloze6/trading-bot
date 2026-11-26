---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4370 USD
---
## Findings
- **F1:** The edge is real but the book captures almost none of it. Inside the falling, agitated profile, shorting every up day of 0 to 1 thirty-day std gives a next-day unusual move of +1.15 % and a total move of +0.97 % (t 2.42, 479 cases, 181 days). Yet the book's mean daily return on days in a position is only 0.035 %, its 425 trades net +0.18 % each, and its mean |allocation| on active bars is 0.14 (median 0.11).
- **F2:** Most up days in the profile are taken at a token size. The mean |allocation| is 0.03 for rises of 0 to 0.25 std, 0.14 for 0.25 to 0.5, 0.24 for 0.5 to 0.75 and 0.35 for 0.75 to 1, and 28 % of in-profile up days within one swing carry |allocation| under 0.05. Each one-day trade still pays the 0.22 % round trip, so the many small cases add cost and dilute the mean daily return.
- **F3:** The stronger case of the situation, a rise of 0.5 to 1 std, also carries the effect longer, while weaker rises fade. With the cases of one day taken together:
- **F4:** The cap at one usual swing is right at every horizon. Rises above 1 std give a short unusual move of +0.28 % at 1 day (t 0.33, 56 days), −0.62 % at 2 days and +0.04 % at 3 days.
- **F5:** The profile is part of the idea's own effect, not a separate effect. The same up days of 0 to 1 std outside the profile give +0.13 % at 1 day (t 0.77, 2336 cases) and +0.09 % at 3 days (t 0.30). Inside the profile without the signal, shorting loses: after down days of −1 to 0 std the short unusual move is −0.77 % at 1 day (t −3.10, 488 cases), and after days below −1 std it is −2.35 % (t −3.85).
- **F6:** The effect points the same way in every year explored, but it rests on few windows.

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days` (from F1, F2, F3, F4, F5, F6): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next three days, only while that rise stays within about one usual swing.
- `058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days` (from F1, F2, F3, F4, F5): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next two days, only while that rise stays within about one usual swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
