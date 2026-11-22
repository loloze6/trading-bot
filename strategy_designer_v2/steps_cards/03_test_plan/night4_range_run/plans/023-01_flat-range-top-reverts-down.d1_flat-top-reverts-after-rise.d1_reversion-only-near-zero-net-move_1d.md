---
idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.d1_reversion-only-near-zero-net-move
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: close far above the middle of the 30-day high-low range, in a month whose net move is small against that range -> replaced: the only graded product of the two, `FlatnessWeightedRangePositionComponent`, measures the range from closes, not from highs and lows.
- Comparison: stronger the closer the 30-day net move is to zero, only while the 90-day return is positive -> kept: graded flatness weight, and a regime rule on the 90-day return being at or above 0.
- Outcome: the price falls over the next 5 days (5 bars) -> kept: short side only, held 5 bars.
- Verdict transfer: no: a result on the closing range would not confirm or reject an idea stated on the high-low range.
Reason: The idea needs range position times flatness, both from the 30-day high-low range, so the short grows with height above the middle and with flatness. Range position (`DonchianBreakoutComponent` "high_low") and the net-move-to-range ratio (`NetMoveToRangeRatioComponent` "high_low") both exist, but the config can only add them in a forecast and multiply them only in the regime detector's on/off gate, so no graded product on the high-low range can be built.
