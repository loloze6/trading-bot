---
line: 7.d confirmed, not profitable
backtest: 060-02_volume-growth-fall-stalls_1d
idea tested: 060-02_volume-growth-fall-stalls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5692 USD
---
## Findings
- **F1:** The tested effect lives only while the fall is still going on in the last weeks. Inside the falling profile, on bars whose 20-day return is negative, the slope of the 5-day excess return on the volume ratio is 0.035 (t 3.63, 426 grid cases), with the quartiles of volume growth graded at -3.21 %, -1.85 %, +0.29 % and +2.44 %. On falling-profile bars whose 20-day return is positive, the slope is -0.021 (t -1.06, 148 cases) and the quartiles show no order (+1.48 %, +0.72 %, +2.59 %, -1.69 %).
- **F2:** The book's gain is lost on the positions held after a 20-day bounce, and earned on the others. Shorts held while the 20-day return was positive lost a summed -0.69 per-bar gain (523 bars, mean -0.13 %), and longs lost -0.24 (388 bars). Shorts held while the 20-day return was negative earned +2.44 (1,582 bars, mean +0.15 %), and longs +1.65 (1,219 bars).
- **F3:** A negative 20-day return is not an effect of its own. On falling-profile grid bars, regardless of volume, it is followed by a 5-day excess of -0.58 % (t -1.06, 426 cases), against +0.78 % (t 0.79, 148 cases) when the 20-day return is positive. With the idea's signal it gives a direction-signed excess of +2.53 % on the shrinking-volume side (t 3.74, 239 cases) and +1.91 % on the growing-volume side (t 2.20, 187 cases). It belongs to the theory, which speaks of "a downtrend that goes on".
- **F4:** Keeping positions only while the recent return is negative changes both failing measures, on an approximate rebuild of the book over folds B and C.
- **F5:** The effect grows with the horizon. Over 10 days, with the 20-day return negative, the slope on the volume ratio is 0.0615 (t 3.45, 207 non-overlapping cases), against 0.035 over 5 days. Over all falling bars it is 0.046 (t 2.75, 274 cases). A move per case nearly twice as large stands against the same 0.19 % trade cost.
- **F6:** The deepest fall of the book (-26.4 %) was in w14, a window where holding the coins lost -52 % in summed daily returns. The book's longs lost a summed -0.85 there while its shorts earned +0.71: longs on growing volume during a sustained crash carried the fall.
- **F7:** Agitation sharpens the cases but does not repair the book.

## Ideas
- `060-02.d1_volume-growth-fall-still-running` (from F1, F2, F3, F4): In a falling market, while the coin's 20-day return is still negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 5 days.
- `060-02.d2_volume-growth-recent-ten-day-fall` (from F2, F3, F4, F6): In a falling market, while the coin's 10-day return is still negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 5 days.
- `060-02.d3_volume-growth-ten-day-hold` (from F1, F3, F5): In a falling market, while the coin's 20-day return is still negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
