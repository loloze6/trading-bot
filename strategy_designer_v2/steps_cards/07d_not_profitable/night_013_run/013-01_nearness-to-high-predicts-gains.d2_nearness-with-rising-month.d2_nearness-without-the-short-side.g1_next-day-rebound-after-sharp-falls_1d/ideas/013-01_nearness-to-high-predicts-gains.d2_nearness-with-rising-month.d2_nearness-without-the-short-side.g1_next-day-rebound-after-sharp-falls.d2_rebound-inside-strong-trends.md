---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day, and the more so the larger the coin's 20-day return in absolute size measured in its own 20-day volatility.
Consequence: A trader buys sharp down days that come inside strong moves either way, and gives less weight to those inside directionless drift, where the next day pays nothing.
Why:
- F6: The rebound pays at the two extremes of the coin's 20-day trend and not in the middle: forecast>0 bars give +0.0035 excess where the 20-day return is −25% and +0.0045 where it is +28%, against −0.00035 and −0.0006 in the two middle quartiles; scaled by volatility, the strongest absolute 20-day moves give +0.0043 (t 3.39) against +0.0005 (t 0.54) for the weakest.
- F5: The book's falls come from being long in calm downtrends: its worst decile of days (−0.023 on average) holds a mean position of 0.68 with a 20-day coin return of −0.048, and the 785 days spent more than 15% under its peak have lower volatility (0.039 vs 0.045), a falling 20-day return (−0.019 vs +0.044) and a larger position (0.26 vs 0.21) than the other days, which pushes the deepest fall to −30.7% and Calmar to 0.43.
- F4: The weak half of the forecast costs more in fees than it earns, dragging the mean daily return under its 0.0005 bar: the two lowest forecast quintiles net −0.000078 and −0.000051 per bar (gain 0.00010 and 0.00021 against fees 0.00018 and 0.00026), while the top two net +0.0016 and +0.0035; overall fees are 0.00035 per bar against a gross gain of 0.00080.
