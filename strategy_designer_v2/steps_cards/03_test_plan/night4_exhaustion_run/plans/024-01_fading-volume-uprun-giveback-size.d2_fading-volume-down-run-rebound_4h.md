---
idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the coin has just fallen in an unbroken streak of 4h bars, with volume declining across the streak -> replaced: no component counts consecutive down closes or reads volume across the streak; only fixed-window returns and volume ratios exist.
- Comparison: the streak's loss against the coin's typical 4h move over the past 30 days -> replaced: the 30-day mean absolute 4h move exists (MeanAbsReturnComponent, 180 bars), but no component gives the loss of a streak of variable length.
- Outcome: rises over the next three days, more after a larger scaled loss -> kept: 18 bars, long, sized by the scaled loss.
- Verdict transfer: no: a fixed-window fall with a fixed-window volume ratio is not an unbroken streak on declining volume, so neither a confirm nor a reject would carry over to the idea.
Reason: The streak and its volume path are in each coin's own bars, and a regime rule or graded component could hold them. No catalogue component counts an unbroken run of down closes, measures that run's loss in typical 4h moves, or measures how volume changed across the run. Fixed-period returns (PriceEvolution, MeanAbsScaledReturn), loss-spread shares (LossShareBeyondLargest) and volume ratios (VolumeRatio) do not combine into a streak of variable length.
