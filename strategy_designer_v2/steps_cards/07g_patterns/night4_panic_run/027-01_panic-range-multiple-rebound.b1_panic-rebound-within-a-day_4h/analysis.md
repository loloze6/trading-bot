---
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
idea tested: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4302 USD
---
## Findings
- **F1:** Over the 4 hours from 20:00 UTC, coins earn less than their usual 4-hour drift (−0.071 %, t −4.62, 17373 bars), and the drop is graded by the coin's own move over the preceding 16:00–20:00 UTC bar. By that move's quintile, from lowest to highest, the next 4 hours return +0.007 % (t 0.18), +0.042 %, −0.041 %, −0.135 % (t −4.03) and −0.189 % (t −4.66), about 3190 bars each. It holds in 5 of 6 coins (BTC t −2.58, XRP t −3.66, ZEC t −2.47) but fades after 2022: 2018 −0.302 % (t −5.44), 2022 −0.171 % (t −4.21), 2024 +0.072 %.
- **F2:** The 16:00–20:00 UTC bar itself returns more than the usual drift (+0.077 %, t 5.15, 17506 bars). It is positive in every year from 2018 to 2025 and in every coin (ETH t 2.86, ZEC t 2.82). So the afternoon rise is partly given back over the next 4 hours.
- **F3:** After a panic (a 24h fall with the 24h range in the top quintile of its 30-day multiple), the following 24–48 hours depend on the first day's outcome. When the first 24 hours rose, the next 24 hours return −0.482 % against the drift (t −2.91, 1045 cases). When they fell, the next 24 hours return +0.518 % (t 2.32, 652 cases). The rebound is paid within a day, and a first-day bounce is partly reversed on the second day.
- **F4:** Within these panics, the deepest quartile of falls carries most of the next-24h excess, +1.786 % (t 5.52, 427 cases), against +0.42 % to +0.93 % for the other three quartiles. The panic premium is positive in every year from 2018 to 2025 (+0.23 % to +1.69 %).
- **F5:** The book's trades lose once they last more than a day. Trades of up to 16 hours make +1.567 % gross (4150 trades) and trades of 16–24 hours +1.823 % (4432). Trades of 1–1.7 days make −0.873 % (2862) and trades over 1.7 days −2.518 % (3255).
- **F6:** Rises with a wide range are followed by lower 24h returns. By range-multiple quintile, from lowest to highest, the next 24 hours return −0.124 %, −0.047 %, −0.138 %, −0.255 % (t −2.13) and −0.309 % (t −2.01). Given how many angles were read, this mirror of the panic effect is only marginal.
- **F7:** The book mostly carries the coins' own moves at about half size. On its worst 2 % of days it loses −8.5 % while the coins fall −11.2 %. Its mean daily return is below holding in every up year (2021: 0.152 % against 0.409 %). It keeps an average allocation of 0.121 on bars with a zero forecast.

## Ideas
- `027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day.g1_late-afternoon-rise-reverses` (from F1, F2): The more a coin rises over the 4 hours from 16:00 to 20:00 UTC, the lower its return over the following 4 hours, from 20:00 to 24:00 UTC.
- `027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day.g2_panic-bounce-second-day-giveback` (from F3, F5, F4): After a panic (a coin falling over 24 hours with a range several times its 30-day average 24-hour range), the more the coin rebounds over the next 24 hours, the lower its return over the 24 hours after that.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
