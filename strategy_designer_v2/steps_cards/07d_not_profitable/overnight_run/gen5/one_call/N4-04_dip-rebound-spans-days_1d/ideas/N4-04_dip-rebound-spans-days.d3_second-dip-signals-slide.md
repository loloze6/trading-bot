---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In an uptrending coin, a sharp one-day drop that is followed by a second sharp drop the next day marks a continuing slide, and price keeps falling over the following days.
Consequence: A trader exits, or does not add, when a dip is followed by another sharp down day instead of averaging into it.
Why:
- F2: Before fees the trades lose: 1432 trades, all long, average −0.06% gross against a 0.10% fee, so −0.16% net. One-bar trades make +1.21% gross (n=1017), but trades held 2–2.5 days lose −3.85% (n=198) and those held 2.5–4.5 days lose −6.15% (n=73). A dip that is followed by further dips, which keeps the forecast positive, is where the losses pile up.
- F1: The book fails on Calmar (0.54 against the 0.75 needed) because its gain and its drawdowns both sit in the fully sized days: days with a position of 1.5–3 (n=703) earn a mean of +1.58% but with a standard deviation of 11.0% and a worst day of −37.6%, while days at ≤0.5 (n=1144) earn +0.01%. Window drawdowns grow from about −5% to −10% in w1–w10 to −12% to −27% in w11–w24 (worst −51% in w12).
