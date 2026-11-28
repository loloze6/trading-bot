---
idea: 089-03_calm-decline-thinning-down-volume
brief: 089_falling-calm-up-volume-lean
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: b5764dedf919
---
Fidelity:
- Situation: in a falling calm market, a coin's average down-day volume over the last 10 days has fallen -> replaced: no component averages volume over down days only.
- Comparison: against its average down-day volume over the 20 days before -> replaced: no component gives a two-window ratio of down-day volume.
- Outcome: the coin rises over the next 5 days, more the larger the fall -> kept: 5 bars long, graded by the fall.
- Verdict transfer: no: overall volume ratios, up-day volume shares and down-streak fades each measure something other than down-day volume against its prior level.
Reason: The idea needs the mean volume of down days (close below the prior close) in the last 10 bars, set against the same mean in the 20 bars before. That uses only the coin's own close and volume, and a single graded value could carry it. No catalogue component computes it. `VolumeRatioComponent` reads every bar's volume. `UpDayVolumeShareComponent` gives a share inside one window, not a level across two windows. `DownStreakVolumeFadeComponent` reads one consecutive streak only. Combining them does not help: the config averages components by weight, but it cannot multiply them or restrict volume to down bars.
