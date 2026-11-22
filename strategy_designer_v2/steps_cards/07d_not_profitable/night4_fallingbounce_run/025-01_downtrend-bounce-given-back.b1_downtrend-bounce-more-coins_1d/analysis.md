---
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4402 USD
---
## Findings
- **F1:** The book's shorts are held well past the idea's 5-day horizon and lose there. Trades last 9.4 days on average. The 2,384 trades of up to 5.5 days lose -0.74 % gross, while those of 5.5–10, 10–20 and over 20 days lose -4.29 %, -7.06 % and -3.67 %. On 55 % of the short bars the forecast is already back at zero, and those bars lose -0.050 % a day against +0.006 % on bars with a live forecast.
- **F2:** The coin's own rise eats the timing gain. On the 16,212 short bars the part from the market's own rise is -0.066 % a day and timing is +0.041 %, so the short bars net -0.025 %. Per case, the total move is -0.14 % against a cost of 0.22 %, even though the unusual move is +0.62 % (t 2.81, 2,312 cases).
- **F3:** The effect sits in shallow 90-day falls and reverses in deep ones. Cases with a 90-day return between -10 % and 0 % have an unusual short move of +2.60 % (t 3.97, 97 cases) and a total move of +1.87 % (t 2.90). Cases between -25 % and -10 % give +1.78 % (t 2.59). Cases below -45 % give -0.96 % unusual and -1.73 % total (119 cases). The book's short bars earn +0.24 % a day at -10 % to 0 % and lose -0.04 % a day below -45 %.
- **F4:** On the 5-day grid of falling coins, forward 5-day returns rise steadily with the depth of the 90-day fall. The deepest quartile (-82 % to -43 %) gains +2.69 % (t 2.79, 221 cases), while the shallowest quartile (-13 % to 0 %) falls -1.68 % (t -3.06, 221 cases).
- **F5:** A moderate 30-day fall marks where the bounce is given back. Short cases with a 30-day return between -30 % and -15 % have an unusual move of +3.04 % (t 6.44, 413 cases), and between -15 % and 0 % +1.37 % (t 3.30). Cases with a 30-day fall beyond -30 % give only +0.83 % (t 0.85), and cases with a positive 30-day return give negative moves (-0.78 % and -0.43 %).
- **F6:** The size of the rise does not grade the fall, except for the very largest rises. The unusual short move is +1.31 % at 0–1 usual moves, +0.53 % at 1–2 and +1.24 % at 2–3, and only rises above 3 usual moves give a clearly larger +5.21 % (t 3.24, 34 cases). The forecast-size correlation is -0.028.
- **F7:** The book loses most in years when the coins rise strongly. It loses -0.16 % a day in 2020 (coins +0.47 % a day) and -0.12 % a day in 2023 (coins +0.32 % a day). On the falling-coin grid those years show forward 5-day returns of +5.22 % (t 7.63) and +1.98 % (t 5.36).

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.d1_bounce-fades-in-shallow-downtrends` (from F3, F2, F6): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the larger that rise in units of the usual daily move and the closer the 90-day return is to zero, the larger the fall.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.d2_bounce-fades-in-ongoing-monthly-decline` (from F5, F2, F3): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the larger that rise in units of the usual daily move, the larger the fall, only while the coin's 30-day return is also negative, the fall being larger the more moderate that 30-day decline.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.d3_deep-falls-rebound-within-days` (from F4, F3, F7): In a coin whose 90-day return is negative, the deeper that 90-day fall, the larger the coin's rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
