---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours, only while its realised hourly volatility over the past 7 days is high against its own level over the past 30 days. Inside that state, the rise is larger the higher that 7-day volatility stands above its 30-day level.
Consequence: A trader takes the evening long only in the coin's turbulent weeks, where the 2-hour rise exceeds a round-trip fee, and stays out in calm weeks where the fee eats the whole edge.
Why:
- F1: The book loses because fees take about five times what the position earns. Summed over all bars, the position's gain before fees is 3.79 and the fees are 18.22. Fees run at 0.107% of the share of the book turned over, and there is about one round trip per day at about 0.5 allocation. So the daily book return is negative for every coin (-0.00061 to -0.00109), while holding the coins returns +0.00067 to +0.00155 a day.
- F3: Almost all of the 2-hour rise sits in the coin's most volatile weeks. In the top decile of 7-day hourly volatility the return is +0.290% (t 4.0, n 1528) and in the ninth it is +0.124% (t 2.5). Deciles 0–7 range from -0.028% to +0.047%, with no t above 1.5. In volatility units it is still the top two deciles that carry it: 0.12 (t 3.6) and 0.09 (t 2.5), against at most 0.05 below.
- F4: Volatility measured against the coin's own recent past tells the same story. In the top quintile of 7-day volatility relative to its 30-day average, the return is +0.145% (t 3.7, n 3050). The other four quintiles range from 0.009% to 0.036%.
- F6: The gain is uneven across years. By year the 2-hour return is +0.138% (t 4.4) in 2020, +0.145% (t 3.8) in 2021 and +0.088% (t 3.0) in 2024. It is -0.053% (t -2.2) in 2023 and about zero in 2018, 2019 and 2025. This fits a gain that shows up only in turbulent periods.
