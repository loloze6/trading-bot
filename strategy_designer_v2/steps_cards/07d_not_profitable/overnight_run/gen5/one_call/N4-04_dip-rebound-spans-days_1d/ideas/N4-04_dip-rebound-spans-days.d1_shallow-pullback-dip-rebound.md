---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Within a coin's 20- and 60-day uptrend, a sharp one-day drop that leaves the close only a few percent below its 20-day high is followed by a rise over the next three days. A drop that has already taken price far below its 20-day high is followed by no such rise.
Consequence: A trader takes the dip only while the pullback from the recent high is still shallow, and refuses dips that come after a deep fall.
Why:
- F5: The rebound comes after shallow pullbacks, not deep ones. When the close is 3–8% below its 20-day high, the 3-bar return is +1.69% (t 3.49, n=411); within 3% of the high it is +0.91% (t 2.32, n=432); 8–15% below it is −0.26% (t −0.38, n=184); more than 15% below it is +0.19% (t 0.12, n=90).
- F1: The book fails on Calmar (0.54 against the 0.75 needed) because its gain and its drawdowns both sit in the fully sized days: days with a position of 1.5–3 (n=703) earn a mean of +1.58% but with a standard deviation of 11.0% and a worst day of −37.6%, while days at ≤0.5 (n=1144) earn +0.01%. Window drawdowns grow from about −5% to −10% in w1–w10 to −12% to −27% in w11–w24 (worst −51% in w12).
- F3: The forecast's information is real but does not grow with forecast size. Over non-overlapping cases, the forward 3-bar return is +0.49% (t 1.18, n=404) for forecasts 0–1, −0.09% (t −0.15, n=224) for 1–5, +2.79% (t 2.30, n=117) for 5–10, +1.42% (t 1.41, n=85) for 10–19.9 and +1.79% (t 3.04, n=314) at the 20 cap.
