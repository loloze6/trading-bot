---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been a moderate share of its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days. The move grows as the net move's share rises toward the middle of its scale and fades as the share nears its top.
Consequence: A trader would follow a coin's 30-day direction for the next 5 days mostly while its trend is still building within its range, and less once the move already spans the whole range.
Why:
- F5: Across all grid bars, the 30-day return's continuation over 5 days is strongest where the 30-day net move covers a quarter to half of the 30-day high-low range: slope t 5.84, directional mean +1.40 %, 1688 cases (t 6.19 over 10 days). It weakens inside the tested regime's band of 0.5–0.75 (t 1.22, 1719 cases) and turns negative at 0.75 and above (t −1.22, 551 cases). The plan's condition therefore selects mostly the part of the data where the effect fades.
- F2: Over longer horizons the slope's t is 2.76 at 10 days (+1.34 %) and 4.52 at 20 days (+2.64 %), but these returns overlap on the 5-day grid, so their t is overstated by about √2 and √4. That leaves roughly 1.9 and 2.3.
- F4: The long side carries the 5-day effect: +1.16 % directional, t 2.73, 1581 cases. The short side gives +0.25 %, t 0.88, 1539 cases.
