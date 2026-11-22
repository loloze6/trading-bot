---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise compared with its 20-day volatility, the more the coin keeps rising over the next 5 days.
Consequence: A trader would follow an unusually large up day for the next 5 days rather than fade it.
Why:
- F4: Large one-day rises are followed by further rises, but large one-day falls are not followed by further falls. On up days, the next 5 days' excess rose with the day's move in units of 20-day volatility (slope 0.0084, t 3.00, n 2867); on down days the slope was flat (−0.0009, t −0.29, n 2865). Days above 2.5 volatilities averaged +5.0 % (t 1.73, n 151). The effect changed sign across years: 2022 −3.4 % and 2025 −3.3 %, against 2023 +2.9 % and 2024 +4.7 %.
