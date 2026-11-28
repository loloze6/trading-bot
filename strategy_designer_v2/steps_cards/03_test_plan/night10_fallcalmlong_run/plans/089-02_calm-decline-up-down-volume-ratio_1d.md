---
idea: 089-02_calm-decline-up-down-volume-ratio
brief: 089_falling-calm-up-volume-lean
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: b5764dedf919
---
Fidelity:
- Situation: a falling, calm market, with the coin's up-day volume lean over the last 20 days -> kept: the profile is added by code, and the lean is graded inside it.
- Comparison: average up-day volume against average down-day volume over the same 20 days -> replaced: the catalogue has only the up days' share of total volume (`UpDayVolumeShareComponent`), which mixes the count of up days into the volume per day.
- Outcome: the coin rises more over the next 5 days (5 bars) -> kept.
- Verdict transfer: no: in a falling market up days are fewer, so a low share of total volume can hide heavy up days, and a test of the share would not decide the per-day ratio.
Reason: The idea compares average volume per up day with average volume per down day. No component computes per-side averages or counts up days, and the config can only take weighted sums of components, so no combination gives that ratio.
