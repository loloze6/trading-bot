---
idea: 026-04_thinner-weekend-larger-reversal
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin's Saturday-Sunday move, read at Sunday's close -> kept: a regime on `WeekdayComponent` and `HourOfDayComponent` picks the bar where Monday 00:00 is next, and the 48-bar return measures the move.
- Comparison: the lower the weekend volume against the preceding five weekdays' volume, the larger the reversed share -> replaced: no component multiplies the weekend move by volume thinness, and a weighted mean cannot make one scale the other.
- Outcome: the move is reversed over Monday and Tuesday, opposite the weekend's direction -> kept: 48 bars held from Sunday's close.
- Verdict transfer: no: a forecast built from the weekend move alone, or added to a volume term, does not test whether thinner weekends are reversed more.
Reason: The idea is an interaction: the size of the reversal bet must grow with weekend thinness. The config can only average components, regimes give steps rather than grades, and score_product only gates a regime, so no catalogue combination gives a weekend reversal scaled by the volume ratio. `VolumeRatioComponent` also cannot set its base to the 120 weekday bars before the weekend, because its base window always reaches bar t or t-1.
