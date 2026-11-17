---
idea: 003-03_heavy-volume-rise-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day rise on volume well above its 30-day average, graded by both size and volume -> replaced: the catalogue can only gate volume with an on/off regime, so the grading by volume is lost.
- Comparison: the day's volume against its own 30-day average daily volume -> kept: VolumeRatioComponent with period 30.
- Outcome: the price keeps rising over the next 5 days, more after larger, heavier rises -> kept: a long position held while the situation shows, judged over 5 bars.
- Verdict transfer: no: a volume gate drops "the heavier its volume, the larger the further gain," so a confirm or reject would not cover the idea as stated.
Reason: The forecast must grow with both the one-day rise and its volume ratio together, as an AND. The config can only average components by weight, so a heavy-volume fall would add to a long and a thin-volume rise would still get a full position. No strategy op or component multiplies the two, and a volume regime gate leaves the volume half on/off.
