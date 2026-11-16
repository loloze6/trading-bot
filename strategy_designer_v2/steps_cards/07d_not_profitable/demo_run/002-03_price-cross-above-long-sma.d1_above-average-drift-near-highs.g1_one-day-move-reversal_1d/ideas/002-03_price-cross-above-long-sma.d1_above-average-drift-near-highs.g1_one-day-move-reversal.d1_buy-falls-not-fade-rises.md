---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its usual daily move, the larger its rise over the next day, only after falls; after a one-day rise, the coin keeps rising over the next five days, more so the larger the rise relative to its usual daily move.
Consequence: A trader would buy a sharp one-day fall in proportion to its size and would not short a sharp one-day rise, but would hold or follow it instead.
Why:
- F1: The book loses on its short side and earns on its long side: positions short after an up day lose a mean -0.001148 per bar after fees (n≈8,853), and longs after a down day gain +0.001038 per bar (n≈8,500), so mean daily net is -0.000074; summing only the long bars' net gives +0.00051 per bar.
- F2: The second half of the tested idea is wrong in this data: in the top decile of one-day rises (mean move 1.91 usual daily moves), the next day's return is +0.18% rather than a fall, so the short loses -0.00185 gross and -0.00295 net per bar; the next-day slope on the size of rises is positive (0.0012, t 1.55, n 8,087), the opposite of reversal.
- F3: The first half holds and is graded: across all falls, the next-day excess return grows with the fall's size (slope -0.0040, t -4.75, n 7,837); the largest-fall decile earns +0.0052 gross and +0.0041 net per bar, and the next two deciles earn +0.0014 and +0.0003 net.
- F4: The bounce after falls holds in both trend states: the next-day slope is t -2.16 (n 3,028) with price above its 50-day average and t -4.12 (n 4,809) below it, while shorts above the 50-day average are the worst group at -0.001926 net per bar (n 4,081).
- F5: Large one-day rises continue rather than reverse over several days: the slope of the excess return on rise size is 0.0047 (t 2.11, n 2,687) over 3 days and 0.0149 (t 3.65, n 1,490 non-overlapping) over 5 days, and it is positive both above (t 2.06) and below (t 2.80) the 50-day average.
- F6: Fees take the whole gain from ordinary days: mean fees (0.000716) exceed mean gross gain (0.000573); in deciles 3 to 7 of the one-day move, gross gain is near zero (-0.00016 to +0.0003) against fees of 0.00043 to 0.00069, so every one of those deciles is net negative.
