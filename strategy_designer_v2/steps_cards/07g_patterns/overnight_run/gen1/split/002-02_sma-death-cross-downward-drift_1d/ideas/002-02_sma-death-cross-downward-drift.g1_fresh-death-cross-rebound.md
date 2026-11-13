---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Shortly after the 50-day SMA crosses below the 200-day SMA, while the spread is still small (short average only slightly under the long), price over the next 10 days rises more often than not and further than the coin's usual drift.
Consequence: A trader would go long, or at least refuse new shorts, in the first weeks after a death cross while the averages are still close together.
Why:
- F2: The strongest forward drift sits in the band just around the cross. In the raw spread decile from −31 to +1 (short SMA barely below the long), the mean forward 10-bar return is +3.12% (t 3.47, 59.5% up), against +0.7% to +0.9% in the four deeper-below deciles.
- F5: The drift is concentrated early after the downward cross and fades with time in the short state. Forward 10-bar returns are +2.15% at 0–10 days since the cross, +2.19% at 10–30 days (t 2.25), +1.15% at 30–60 days and +0.13% at 60–120 days.
- F10: The 1273 short trades lose on price, not fees. The mean adverse price move is −11.2% against 0.20% mean commission, with a 23.6% win rate. The worst losses come from trades held 23–55 days (mean −19.1%) and from entries at a weak forecast of −5 to −2 (mean −16.6%, against about −10.5% for deeper entries).
