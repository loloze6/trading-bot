---
idea: 068-02_falling-agitated-run-break-fade
brief: 068_falling-agitated-first-bounce-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 78914cf300b5
---
Fidelity:
- Situation: a day that closes up, after an unbroken run of down days ending just before it -> replaced: no catalogue component can measure it. The down-streak count at that day reads 0 on an up day, and no component or op reads it at the bar before.
- Comparison: the longer the run of falls before the bounce, the larger the fall -> adapted: graded by the run length, which is the quantity that cannot be computed.
- Outcome: the coin falls over the next day -> kept: a short held 1 bar.
- Verdict transfer: no: without the length of the down run that ended the day before, no config measures the idea's situation.
Reason: The idea needs, on an up-closing day, the length of the run of down closes that ended on the bar before. `UpCloseStreakLengthComponent` (`side` "down") and `DownStreakLossInUsualMovesComponent` read the streak ending at bar t, so they are 0 on that up day, and they have no `lag`. No transform reads a component's previous value either, because `standardise` must be the only history op. Vetoes with `consecutive_bars` also count runs that end at bar t, not runs that end before it.
