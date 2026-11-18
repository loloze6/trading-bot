---
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds_1d
idea tested: 003-02_thin-volume-drop-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3437 USD
---
## Findings
- **F1:** The book barely earns: a mean daily return of 1.9e-5 and a Sharpe of 0.09, against holding Sharpes per coin of 0.26 to 0.65. Average exposure per window was only 3–10 %, and the mean gross trade P/L was negative on BTC (−0.40 %), ETH (−0.14 %), LTC (−0.09 %) and ZEC (−0.62 %).
- **F2:** Thin-volume down days give no rebound; they keep falling. On the 10-day grid they show an excess return of −0.70 % over 2 days (t −2.27, n 395) and −0.89 % over 5 days (t −1.84). Up days show +0.54 % over 5 days (t 1.26).
- **F3:** The loss comes almost entirely from coins trading below their 50-day average. There, thin-volume down days lead to an excess 5-day return of −3.12 % (t −5.04, n 170). Above the average the same days give +0.06 % (t 0.07, n 134), and heavy-volume down days below the average give −0.94 % (t −0.73, n 92).
- **F4:** The coin's 60-day return grades this. For thin-volume down days, the excess 5-day return is −3.89 % in the lowest 60-day-return tercile (t −4.48, n 81), −2.92 % in the middle tercile (t −3.30, n 84) and +1.23 % in the top tercile (t 1.05, n 86).
- **F5:** On the book's own 5-day grid, active cases below the 50-day average lost −1.06 % excess (t −2.21, n 372), while those above it made +0.06 % (n 271). Every forecast quartile was negative (−1.10 % to −0.50 %), so the forecast's size does not grade the outcome.
- **F6:** Active cases in the calmest 20-day volatility quartile lost −1.24 % excess over 5 days (t −2.39, n 228), while the most volatile quartile made +0.30 % (t 0.36, n 227).

## Ideas
- `003-02_thin-volume-drop-rebounds.d1_thin-drops-rebound-in-uptrends` (from F3, F4, F5): When a coin falls sharply over one day on volume well below its own 30-day average daily volume, it wins back part of that fall over the next 5 days, only while its 60-day return is positive. The larger the fall, the thinner its volume and the higher its 60-day return, the larger the rebound.
- `003-02_thin-volume-drop-rebounds.d2_quiet-drops-extend-downtrends` (from F2, F3, F4): When a coin whose 60-day return is negative falls over one day on volume below its own 30-day average daily volume, it keeps falling over the next 5 days. The further its 60-day return is below zero, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
