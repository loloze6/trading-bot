---
line: 7.g patterns
backtest: 041-02_agitated-fall-rise-vs-range-giveback_1d
idea tested: 041-02_agitated-fall-rise-vs-range-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3945 USD
---
## Findings
- **F1:** In the falling agitated profile, the next-day excess return falls as the day's close-to-close move against the prior 30-day mean daily range grows: the slope is −0.0227 (t −3.93, day-clustered, 1,022 cases on 343 days). By decile of the scaled move, the lowest two deciles are followed by +2.88 % (t 2.21) and +1.85 % (t 2.54), and the highest by −2.23 % (t −2.46).
- **F2:** In that profile the reversal is carried by down-days only. On down-days the slope is −0.0269 (t −3.06, 522 cases, 214 days); on up-days it is −0.0015 (t −0.15, 500 cases, 195 days). The rise-gives-back side tested here has no grading, which matches the verdict's slope t of −0.52.
- **F3:** The down-day bounce in the profile is graded by quartile of the scaled fall. The next-day excess return is +1.93 % for the largest falls (mean −1.08 ranges) and +1.76 % for the next quartile, against +0.63 % and +0.64 % for the two smallest. The largest-fall move is about 10 times the 0.19 % cost of a trade.
- **F4:** The down-day grading is specific to the profile. Outside it, the same down-day slope is +0.0016 (t 0.22) in falling non-agitated markets, −0.0130 (t −1.02) in choppy markets and −0.0096 (t −1.36) in rising markets.
- **F5:** The effect is spent after one day. In the profile, the scaled move's slope on the day-2 excess return is +0.0076 (t 1.43). Days 3 to 5 show no ordered pattern across deciles (all |t| < 2).
- **F6:** The profile's down-day slope is negative on all six coins: BTC −0.020 (t −5.4), ETH −0.043 (t −3.1), XMR −0.028 (t −2.1), LTC −0.048 (t −1.9), ZEC −0.023 (t −1.9), XRP −0.019 (t −0.9).
- **F7:** The down-day slope is not steady across years: −0.016 (t −0.9) in 2018, −0.011 (t −0.7) in 2019, −0.035 (t −8.3) in 2020 and +0.0003 (t 0.03) in 2021.
- **F8:** A low close in the day's range in the profile is followed by +2.14 % (t 2.52, lowest fifth of close location). On down-days this adds nothing once the scaled fall is known: the close-location slope on the residual is −0.0002 (t −0.01). It is the same effect, not a second one.
- **F9:** The tested short book earns on days the coins fall and loses on days they rise. Its best twentieth of days averages +1.14 % while the coins fall −4.61 %. Its worst twentieth averages −0.87 % while the coins rise +4.09 %. It is a short exposed to the profile's rebounds, which is the side F2 says carries no reversal.

## Ideas
- `041-02.g1_agitated-fall-down-day-range-bounce` (from F1, F2, F3, F4, F5, F6): In a falling, agitated market, the larger a coin's one-day fall against its 30-day average daily range, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
