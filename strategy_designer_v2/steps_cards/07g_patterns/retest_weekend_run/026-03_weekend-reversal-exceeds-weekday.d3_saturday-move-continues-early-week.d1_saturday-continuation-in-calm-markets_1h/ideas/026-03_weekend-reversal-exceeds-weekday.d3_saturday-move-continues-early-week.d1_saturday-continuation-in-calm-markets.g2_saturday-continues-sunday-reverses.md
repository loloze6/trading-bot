---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday 24-hour return and its Sunday 24-hour return both point to the move over the next two days, Monday and Tuesday: that move follows Saturday's direction and goes against Sunday's. The larger Saturday's move is against Sunday's, the larger the move in Saturday's direction.
Consequence: A trader would take Monday's position from the gap between Saturday's and Sunday's moves, rather than from either day alone.
Why:
- F4: Saturday and Sunday act in opposite directions on Monday–Tuesday: in a joint regression of the 48-hour return (1910 cases) on both days' volatility-scaled moves, Saturday's coefficient is +0.0094 (t 4.31) and Sunday's is −0.0047 (t −2.31). The two days' moves are nearly uncorrelated (−0.08). The tested continuation sits on Saturday, while the brief's reversal sits on Sunday.
- F1: Sunday's 24-hour move is reversed over Monday and Tuesday: across 1910 Sunday cases the de-drifted 48-hour return against Sunday's direction averages +0.84 % (t 5.06, strength 0.131), and it is positive in every year 2018–2025 (from +0.03 % to +1.82 %) and for every coin (from +0.48 % to +1.21 %).
- F8: The tested Saturday continuation is not stable over time. Its de-drifted 48-hour move is −0.03 % in 2021 and −0.82 % in 2025 (t −2.00, 252 cases), and −0.28 % for ZEC. The book lost in those same years: −3.1 bp a day in 2021 and −1.1 bp a day in 2025.
