---
line: 7.d confirmed, not profitable
backtest: 058-03.b1_calm-rise-continuation-all-coins_1d
idea tested: 058-03.b1_calm-rise-continuation-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6980 USD
---
## Findings
- **F1:** The book's deepest fall, which is what failed the Calmar test, comes in w11: it drops 17.7 % over 386 days while its coins' mean fell 72.6 %, and in w12 the held bars lost money on every one of the 9 coins held (sum of daily gains −0.84). In these two windows, held bars whose close stood 10–25 % above the 20‑day average lost 0.33 % a day (112 bars) and those above 25 % lost 0.69 % a day (23 bars), while those within 10 % gained 0.33 % a day (186 bars).
- **F2:** Over folds B, C the gain grows with the distance above the 20‑day average only up to a point, then turns negative. On the held bars, the mean daily gain rises from +0.42 % (0–5 %, t 4.7) to +0.60 % (15–25 %, t 1.7), then falls to −0.10 % above 25 % (99 bars, t −0.2), the bars that carry the largest losses. On the 5‑day grid, signal cases above 25 % show an unusual move of −1.64 % (14 cases, t −0.68), against +3.39 % for those at or below 25 % (148 cases, t 3.49).
- **F3:** The extreme distance is not an effect of its own. Grid bars more than 25 % above the average without the signal (outside the rising‑calm profile) show +1.0 % over 5 days (21 cases, t 0.37), not the signal's −1.64 %. The fade belongs to the idea's own situation: per the brief's theory, the far end of a run is where steady buying gives way to fragile chasers.
- **F4:** Removing the positions held more than 25 % above the average lifts the B, C book's Calmar from 1.55 to 1.76. The deepest fall eases from −17.4 % to −15.9 %, the yearly return rises from 27.0 % to 28.0 % and the Sharpe from 1.32 to 1.45.
- **F5:** The 5‑day holding loses and the long holdings earn. The 353 trades of at most 5.5 days lose 2.39 % each after fees (sum −844 %). The 123 trades of 10–20 days earn +15.9 % each and the 49 trades over 20 days earn +33.9 %.
- **F6:** Over 10 days, signal cases still carry the effect. Cases 0–5 % above the average show an unusual move of +5.7 % (36 cases, t 2.26) and cases 10–20 % above show +6.4 % (38 cases, t 3.20). The 5‑day idea's whole size is +0.41 % (t 0.67) against a 0.22 % cost per trade, so a longer holding captures more move per trade paid.
- **F7:** Other cuts do not fix the falls. Leaving out bars with a high 10‑day/60‑day swing ratio (above 1.2) eases the deepest fall to −15.8 %, but the yearly return drops to 24.3 % and the Calmar to 1.54. Held bars after a 60‑day rise above 60 % earn 0.03 % a day (129 bars, t 0.11), yet their 5‑day grid cases show +4.3 % (23 cases), so a long 60‑day run is not a cut.

## Ideas
- `058-03.b1.d1_calm-rise-moderate-stretch` (from F1, F2, F3, F4): In a rising, calm market, the further a coin's close stands above its 20-day average price, the more the coin rises over the next 5 days, the rise growing with a moderate distance and fading back to a giveback as the distance becomes extreme for the coin.
- `058-03.b1.d2_calm-rise-longer-hold` (from F5, F6): In a rising, calm market, the further a coin's close stands above its 20-day average price, the more the coin rises over the next 15 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
