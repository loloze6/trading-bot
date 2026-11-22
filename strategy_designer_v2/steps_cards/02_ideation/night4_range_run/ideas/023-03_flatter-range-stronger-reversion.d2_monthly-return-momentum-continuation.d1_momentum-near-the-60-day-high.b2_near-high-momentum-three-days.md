---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
line: 7.b inconclusive
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 3 days, the more so the closer the coin's close stands to its highest close of the past 60 days.
Consequence: A trader leans long on monthly strength near the 2-month high for a few days, not a week, and trusts monthly weakness far from that high least.
Why:
- F1: On the plan's 5-day grid the forecast's slope is on the predicted side but small and noisy (slope 0.000273, t 1.30, 3,419 cases). The same forecast is clear over shorter horizons (t 2.30 at 1 day on 17,380 cases, t 2.51 at 3 days on 5,723) and fades over longer ones (t 0.46 at 10 days, t −0.11 at 20 days), so the plan read the idea past the horizon where it shows.
- F2: Over 3 days, the idea's own product of 30-day return and nearness to the 60-day high is clearer than at 5 days. The raw product has t 3.42 (2,843 cases) against t 1.47 at 5 days (1,691 cases), and the recorded raw component has t 3.26 against t 1.80. The standardisation over the past 60 values weakens it (post-pipeline t 2.51 at 3 days, 1.30 at 5 days; correlation of post-pipeline with raw 0.30).
- F4: The gain sits on the long side near the high. Five-day excess returns in the forecast's direction are +1.35 % (t 2.78, 516 cases) after a 30-day rise in the third of cases nearest the 60-day high, and −0.10 % (t −0.16, 370 cases) after a rise further from it. Within the forecast's short side the slope is the wrong way (t −1.44, 1,703 cases), against t +0.44 on the long side.
