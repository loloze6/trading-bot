---
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
idea tested: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4552 USD
---
## Findings
- **F1:** The fade is real against the coin's drift but not in price: over the 2419 short cases the coin's 5-day move in the short direction is −0.19 % in total (t −0.84) and +0.55 % unusual (t 2.50). The book pays the total move, and that sits below zero before the 0.22 % cost of a trade, so the book loses (Sharpe −0.32, mean daily return −0.0002).
- **F2:** The losses come from years when the coins were rising. Short cases lost −4.10 % over 5 days in 2020 (t −4.50, n 141), −2.25 % in 2021 (t −2.24) and −2.03 % in 2023 (t −4.12). The coin's mean daily return in those years was +0.44 %, +0.54 % and +0.32 %. The cases gained in 2018, 2022 and 2025 (+0.74 %, +0.46 %, +2.19 % with t 4.37), when the coin's mean daily return was −0.35 %, −0.24 % and −0.03 %.
- **F3:** The fade grows with the 90-day fall only up to a point, then turns. In the deepest 90-day-fall quintile (−80 % to −43 %) the cases lost −1.17 % over 5 days (t −2.02) and −2.85 % over 10 days. The middle quintile (−28 % to −19 %) gave +0.57 % in total and +1.33 % unusual (t 2.93).
- **F4:** Net trades average −2.72 % (median −1.19 %, 4228 trades). Their mean length is 9.4 days against the 5-day horizon, and the cases' total short move worsens from −0.19 % at 5 days to −0.35 % at 10 days. Holding past the horizon adds loss.
- **F5:** In coins outside the falling regime, a one-day rise of more than 2 usual daily moves is followed by a further rise of +5.25 % over 5 days (t 4.84, n 495), or +4.46 % beyond drift (t 4.13). That is about 24 times the cost of a trade, and it is the opposite of what follows bounces in falling coins.
- **F6:** The size of the rise does not grade the fade cleanly. Total 5-day short moves by quartile of the day's scaled rise are +0.45 %, +0.46 %, −0.77 % and +0.72 %, so only the largest rises carry a fade (+1.50 % unusual, t 2.72).

## Ideas
- `025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins.d1_fade-bounces-in-yearly-downtrends` (from F1, F2, F4): In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The more negative the coin's 365-day return, the larger the fall that follows.
- `025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins.d2_fade-shrinks-in-crashed-coins` (from F3, F1): In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The fall is largest where the 90-day fall is moderate, and it shrinks as the 90-day fall deepens into a crash.
- `025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins.d3_bounces-extend-in-uptrends` (from F5, F6): In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days. The larger the rise against its usual daily move, the larger the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
