---
line: 7.d confirmed, not profitable
backtest: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks_1d
idea tested: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7465 USD
---
## Findings
- **F1:** The book fails Calmar (0.18 against 0.75) because one fall of 40.9 % runs from w14 into w15. In w14 the book lost 0.31 % a day while holding 0.84 of its value on average. Every coin held lost: BTC −12.6 %, ETH −6.4 %, XMR −6.3 %, LTC −6.1 %, ZEC −5.6 % of the book. Its 35 trades averaged −17.7 % net, and its three grid signals were all weak scaled rises (raw 7-day rise ≤ 0.5 of a usual swing), which moved −29.6 % unusual over 14 days.
- **F2:** The weak cases of the signal lose and the strong ones carry the effect. On the 14-day grid in the profile, raw scaled rises ≤ 0.5 moved −14.5 % unusual (13 cases, t −2.20), and rises > 0.5 moved +18.3 % (25 cases, t 1.50). Trades entered on a raw scaled rise ≤ 0.5 averaged −3.84 % net (36 trades). Rises of 0.5–1.0, 1.0–1.5 and > 1.5 averaged +7.0 %, +10.1 % and +7.3 % (56, 56 and 107 trades). The standardised forecast gives these small rises a positive size: the lowest forecast tercile averaged −13.0 % unusual (14 cases, t −2.05).
- **F3:** The strong scaled rise is not an effect of its own. Outside the profile, the same raw scaled rises > 0.5 moved −0.14 % unusual over 14 days (119 cases, t −0.04). In the profile without a signal, coins moved −3.2 % (38 cases, t −0.79). The continuation lives only where the theory puts it: in quiet, trendless coins.
- **F4:** The move keeps building past 14 days. Strong in-profile signals moved +30.2 % unusual over 28 days (t 1.88), against +18.3 % over 14. Trades held 20–30 days averaged +14.4 % net (66) and those held over 30 days +18.7 % (40). Trades held 10–15 days averaged −4.6 % (104).
- **F5:** The first week after the signal tells which trades lose. Trades whose first 7 days fell more than 10 % averaged −17.9 % net (35 trades); those that rose more than 10 % averaged +20.1 % (56). On the grid, signals whose first week rose more than 5 % moved +11.1 % unusual in the second week (15 cases, t 1.07). The same first-week rise without the signal gave +1.4 % (225 cases, t 0.61), so the first-week path alone carries no effect.
- **F6:** The book does not beat holding (Sharpe 0.47 against holding's 0.55) because, over all folds, the idea's unusual move per case is −0.14 % (t −0.14, 581 cases). Its total move is +2.06 % per case, 9.2 times the 0.22 % cost, but that gain is mostly the coin's own drift. The weak cases dilute the effect: in the explored folds the signal grid moved +6.4 % unusual over 14 days (42 cases), and the strong cases alone moved +18.3 %.
- **F7:** The gain is concentrated in a few coins: XRP made +898 % summed net over 41 trades and ADA +459 % over 19, while XMR lost −343 % over 60. By year, signals averaged −29.4 % unusual in 2018 and −11.1 % in 2019, against +18.8 % in 2020 and +12.8 % in 2021. The effect is uneven over time but not one window's.

## Ideas
- `059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation` (from F1, F2, F3, F6): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, the larger its further rise over the next 14 days. The further rise comes from rises that are large against the coin's own swing, while a rise small against that swing gives back over the same 14 days.
- `059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks` (from F3, F4, F6): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, the larger its further rise over the next 28 days.
- `059-01.b1.b1.d1.b1.b1.d3_choppy-calm-confirmed-rise-continues` (from F1, F5, F3): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, the larger its rise in the second week after it. The rise is larger the more the coin kept rising in the first week after the signal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
