---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall.
Consequence: Weekend rises are partly undone once weekday liquidity returns.
Why:
- F1: The main measure is positive (mean gain 0.00646, t 2.75, 1268 cases), but the supporting check fails because the size grading runs backwards. Sunday rises in the smallest-z quintile (mean z 0.11) are followed by a 2-day excess return of −0.0158. The largest-z quintile (mean z 2.21) is followed by only −0.0037, and the steps between are monotone (−0.0124, −0.0097, −0.0072). So the large-minus-small difference is +0.0035.
- F2: The reversal is specific to Sunday. Rises stamped Sunday are followed by a 2-day excess of −0.0098 (t −4.26, n 1083). Rises on other weekdays are followed by between −0.0025 and +0.0022 (|t| ≤ 1.2), except Thursday at +0.0088.
- F5: The reversal after Sunday rises shows in four of six coins: ETH −0.0132 (t −2.84), LTC −0.0127 (t −2.16), XMR −0.0118 (t −2.57) and ZEC −0.0161 (t −2.42). It is nearly absent in BTC (−0.0013, t −0.30) and XRP (−0.0027, t −0.36).
