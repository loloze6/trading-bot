---
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
idea tested: N4-04_dip-rebound-spans-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3346 USD
---
## Findings
- **F1:** The book fails on Calmar (0.54 against the 0.75 needed) because its gain and its drawdowns both sit in the fully sized days: days with a position of 1.5–3 (n=703) earn a mean of +1.58% but with a standard deviation of 11.0% and a worst day of −37.6%, while days at ≤0.5 (n=1144) earn +0.01%. Window drawdowns grow from about −5% to −10% in w1–w10 to −12% to −27% in w11–w24 (worst −51% in w12).
- **F2:** Before fees the trades lose: 1432 trades, all long, average −0.06% gross against a 0.10% fee, so −0.16% net. One-bar trades make +1.21% gross (n=1017), but trades held 2–2.5 days lose −3.85% (n=198) and those held 2.5–4.5 days lose −6.15% (n=73). A dip that is followed by further dips, which keeps the forecast positive, is where the losses pile up.
- **F3:** The forecast's information is real but does not grow with forecast size. Over non-overlapping cases, the forward 3-bar return is +0.49% (t 1.18, n=404) for forecasts 0–1, −0.09% (t −0.15, n=224) for 1–5, +2.79% (t 2.30, n=117) for 5–10, +1.42% (t 1.41, n=85) for 10–19.9 and +1.79% (t 3.04, n=314) at the 20 cap.
- **F4:** The rebound disappears in the most volatile state. By coin-wise 20-day volatility tercile, the forward 3-bar return is +0.83% (t 2.11, n=358) when calm, +2.05% (t 4.18, n=357) in the middle and +0.49% (t 0.81, n=361) when wild, with days 2–3 at −0.03% (t −0.06). The wild tercile's active book days have a standard deviation of 9.0% and a worst day of −33.5%.
- **F5:** The rebound comes after shallow pullbacks, not deep ones. When the close is 3–8% below its 20-day high, the 3-bar return is +1.69% (t 3.49, n=411); within 3% of the high it is +0.91% (t 2.32, n=432); 8–15% below it is −0.26% (t −0.38, n=184); more than 15% below it is +0.19% (t 0.12, n=90).
- **F6:** The losses are concentrated in two coins: LTC (−0.88% net per trade, n=277) and ZEC (−0.92%, n=242, worst trade −55.8%). BTC, ETH, XMR and XRP are positive net, from +0.08% to +0.56%.

## Ideas
- `N4-04_dip-rebound-spans-days.d1_shallow-pullback-dip-rebound` (from F5, F1, F3): Within a coin's 20- and 60-day uptrend, a sharp one-day drop that leaves the close only a few percent below its 20-day high is followed by a rise over the next three days. A drop that has already taken price far below its 20-day high is followed by no such rise.
- `N4-04_dip-rebound-spans-days.d2_dip-rebound-needs-moderate-volatility` (from F4, F1): In an uptrending coin, a sharp one-day drop is followed by a rise over the next three days when the coin's recent daily volatility is moderate. When recent volatility is in its highest third, the drop is followed by a larger spread of outcomes around a flat mean.
- `N4-04_dip-rebound-spans-days.d3_second-dip-signals-slide` (from F2, F1): In an uptrending coin, a sharp one-day drop that is followed by a second sharp drop the next day marks a continuing slide, and price keeps falling over the following days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
