---
idea: 003-05_up-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Every bar has two parts. The move is the 1-day close-to-close return (PriceEvolutionComponent, period 1), standardised over its past 60 values (min 20), with the down side set to 0 (clip min 0), and passed through signed_power with exponent 2 and pivot 10, so sharp up days count more and small ones are damped smoothly towards 0. The volume condition compares the bar's volume with its 20-bar mean. - On a low-volume bar (volume below the 20-bar mean), the forecast is minus that graded up-move value: a short that grows with the size of the thin rise. - On a high-volume bar (volume at or above the mean), the forecast is plus the same value: a long that grows with the size of the heavy rise. - On a down day or a flat day, the forecast is 0. - The position is held for the next bar only. It changes with the next bar's move and volume.
Config: 003-05_up-move-retrace-by-volume_1d_config.json
Confirm: The horizon is 1 bar. Take every up-move bar with a non-zero forecast, pooled over all 6 windows; each daily return is counted once because the holds do not overlap. For each such bar, take the next bar's return minus the coin's mean daily return in that window, and weight it by the size of the up-move value |forecast|. The confirming result is that the weighted mean on high-volume bars exceeds the weighted mean on low-volume bars, with a two-sample t-statistic of at least 2.0. Supporting check: the config's portfolio return before costs is positive in at least 4 of the 6 windows.
Reject: The weighted mean excess next-bar return after low-volume up moves is equal to or higher than after high-volume up moves (difference ≤ 0). The idea is also rejected if the difference is positive but has t ≤ 1.0 while each group holds at least 60 bars.
Inconclusive: A positive difference with t between 1.0 and 2.0. Also any result where either volume group has fewer than 60 up-move bars across the 6 windows.
Deviation: - "Afterwards" is fixed at the next daily bar, not a longer giving-back period. - A "sharp move" is a single day's rise, graded by size (squared) rather than selected by a threshold. - "Unusually low or high volume" becomes a binary split at the 20-bar mean volume. - The idea is a relative claim, but the config bets in opposite directions in the two groups. Its PnL therefore also reflects absolute reversion and continuation; the criterion judges only the difference between the groups.
