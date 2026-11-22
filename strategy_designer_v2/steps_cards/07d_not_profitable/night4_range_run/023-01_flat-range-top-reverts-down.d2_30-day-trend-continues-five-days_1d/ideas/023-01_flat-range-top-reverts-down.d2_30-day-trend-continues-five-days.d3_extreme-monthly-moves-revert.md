---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return has been extreme relative to its 30-day high-low range, the larger that 30-day return, the further the coin moves back against it over the next 5 days.
Consequence: A trader would stop following a 30-day move once it is extreme and would expect part of it to come back.
Why:
- F2: Inside w3–w10 the short side carries the loss: shorts sum -2.35 (mean -0.00131 per bar, 1795 bars) and longs only +0.33. Outside that stretch shorts sum +2.02 and longs +12.10, and over all windows shorts make nothing (mean -0.00006 over 5173 bars against +0.00232 for longs).
- F4: The book loses when the 30-day move it follows is already extreme. Positions whose 30-day return in their direction is above 35 % earn -0.00066 per bar (t -0.73, 2039 bars), against +0.00251 (t 2.9) for 22–35 %. Shorts after a 30-day fall of more than 35 % lose -2.50 in sum (mean -0.00384, 652 bars).
