---
idea: 003-02_low-volume-down-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp one-bar drop on unusually low volume -> adapted: low volume becomes a regime veto (bar volume below its 20-bar mean), and the drop is graded by the size of the one-bar fall.
- Comparison: bar volume against its usual level -> adapted: compared with the 20-bar mean volume, the only volume comparison the config offers, so "unusually" becomes "below average".
- Outcome: price rebounds, recovering part of the drop -> adapted: the long position is held only while the low-volume drop bar is current, so the rebound is judged on the next bar.
- Verdict transfer: yes: the forecast is long, sized by how far price fell, only on thin-volume falling bars, so a next-bar rebound or its absence is the idea's own claim.
Forecast: The detector sends a bar to the mean_reversion regime when its volume is below its 20-bar mean. On every other bar the forecast is 0. In that regime, one component carries the signal. It takes the one-bar percent return, standardises it against its own past 60 values, flips its sign and clips it at 0. The forecast is therefore positive only when the low-volume bar closed down. It grows in proportion to the size of the drop relative to recent one-bar moves, about +10 for a typical-size fall and up to +20 for twice that or more. It is 0 on up bars and on bars with normal or high volume. It is long only, because the idea is about rebounds after drops.
Config: 003-02_low-volume-down-move-reverts_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's return over the next bar, weighted by the forecast on each active bar (forecast > 0). It is compared with the coin's unconditional mean one-bar return over all bars of the same window, so the market's own rise is not credited to the idea. All six windows are pooled, before costs.
- Supporting check: The mean next-bar excess return on active bars in the top quintile of forecast, minus the same on the bottom quintile.
- Confirm: The pooled forecast-weighted excess return is above 0 with t ≥ 2 (each 1-bar return is counted once). It is positive in at least 4 of the 6 windows. The top-quintile excess also exceeds the bottom-quintile excess.
- Reject: The pooled excess return is ≤ 0. Or the top-quintile excess is ≤ 0 or below the bottom-quintile excess, meaning thin-volume drops hold or extend.
- Inconclusive: A pooled excess return above 0 with t below 2, or windows that split 3 and 3. Any result based on fewer than 300 active bars pooled, or fewer than 60 in the top quintile, is also inconclusive.
