---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h
idea tested: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3392 USD
---
## Findings
- **F1:** The book is mostly a geared long on the coin, not a timing book: it holds a position on 86 % of bars with a mean allocation of 0.77. Of its mean hourly gain of 0.0058 %, the market's own rise accounts for 0.0045 % and timing for only 0.0014 %. It therefore trails holding, with a Sharpe of 0.578 against 0.636 and a mean daily return of 0.104 % against 0.127 %.
- **F2:** The book's deepest falls are the coins' bear stretches: −66 % over 309 days in w1–w3 (coin −70 %), −62 % over 270 days in w12–w14 (coin −78 %) and −45 % in w21–w22 (coin −49 %). In w16–w17 the book fell −68 % against the coin's −37 %, and in w23–w24 −60 % against −33 %, which gives a Calmar of 0.249.
- **F3:** When the coin's 30-day return is negative (47 % of bars), the book still holds a mean allocation of 0.68 and is in on 83 % of bars, while the coin returns −0.0025 % an hour and the book −0.0039 % an hour. When the 30-day return is positive, the allocation is 0.84 and the book earns +0.0132 % an hour.
- **F4:** After a 30-day fall, volume-surge rises reverse rather than continue: across 1460 cases the strength is −0.064 over 3 hours (t −2.05) and −0.080 over 12 hours (t −2.61). After a 30-day rise, 1853 cases show +0.040 over 24 hours (t 1.86).
- **F5:** Graded by the 30-day return, the 24-hour unusual move rises from −0.21 % in the second quintile to +0.17 % in the fourth and +0.26 % in the top quintile (above +22 %), with a strength of 0.062 and t 1.64. That top quintile's total move of +0.41 % is 3.7 times the 0.11 % trade cost, against 0.6 times for the unusual move over all cases.
- **F6:** The forecast's own size does not grade the move. The lowest forecast tercile has a strength of 0.041, the middle −0.005 and the top (forecast 8.6–20, 2669 cases) 0.014. Over all 4448 cases the unusual move is only +0.07 % per case against a 0.11 % cost.
- **F7:** The cases lose in the falling years, with a 24-hour unusual move of −0.37 % in 2018, −0.18 % in 2022 and −0.27 % in 2025, and gain +0.51 % in 2020 and +0.35 % in 2021.

## Ideas
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day.d1_volume-surge-rises-in-uptrends` (from F2, F3, F4, F5, F7): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 30-day return is positive, and the further rise is larger the higher both that hour's volume against its 30-day average and the coin's 30-day return.
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day.d2_downtrend-volume-surge-rises-fade` (from F3, F4, F7): In a coin whose 30-day return is negative, an hour that rises far more than its typical hourly move over the past 30 days on volume several times its 30-day average is followed by a fall over the next 12 hours, and the fall is larger the deeper the coin's 30-day decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
