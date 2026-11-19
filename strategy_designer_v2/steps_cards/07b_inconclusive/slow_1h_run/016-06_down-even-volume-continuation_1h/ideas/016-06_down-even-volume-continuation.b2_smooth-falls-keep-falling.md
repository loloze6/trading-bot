---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the more of its hourly price path went in the fall's direction (its 3-day net move as a share of its summed hourly moves), the more it keeps falling over the next 3 days.
Consequence: A smooth hour-by-hour decline is a reason to stay short or stay out over the next 3 days, while a choppy fall of the same size is not.
Why:
- F5: How smooth the fall was in price, rather than in volume, shows a borderline link to continuation at the plan's horizon. Path efficiency is |net 72h log move| / sum of |hourly log moves|. Controlling for the fall's size, higher efficiency is followed by lower 72h excess returns (t −2.06, n 2,669). The link is weaker at 24 hours (t −1.17) and 168 hours (t −0.85).
- F1: Among the 2,669 to 2,762 non-overlapping 72-hour grid cases where the coin had fallen over the past 3 days, the volume evenness measure ln(mean/median) has no link to the next 3 days' excess return, so the forecast's slope of 0.00134 (t 0.94) is effectively zero rather than a small effect on the predicted side. The concentration slope alone has t 0.05, and t −0.30 once the size of the fall is controlled. It also has no link at 24 hours (t 0.95) or 168 hours (t −0.10).
