---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin's close sits to its 90-day high, the larger its rise over the next 5 days above its normal drift.
Consequence: A trader should hold a coin longer, and larger, the closer it trades to its 90-day high, since the long side carries this effect's gain.
Why:
- F1: The short side is what loses. On the 8824 short bars the book lost -0.000255 per bar, and -0.000260 of that is simply the coin's own rise against the position, because the coins rose +0.087 % a day while it was short. Shorts carried -54 % of the book's total gain. On the 8458 long bars the book gained +0.000756 per bar, of which only 0.000328 came from the market's rise, so timing was about +0.00043.
- F3: The unscaled 20-day return predicts the next 5 days better than the components the book uses. Its slope t is 2.69 (2843 non-overlapping cases), against 2.31 for the standardised nearness to the 90-day high, 1.40 for the 20-day return standardised over 60 days, and 1.90 for the combined forecast (3419 cases).
- F5: The book is too small and too split to beat holding:
- F6: Most of the forecast's spread sits at its top. Across forecast quintiles the 5-day excess return goes from -0.35 % and -0.37 % in the two lowest quintiles to +0.27 % and +0.61 % in the two highest, so the long end carries the larger move.
