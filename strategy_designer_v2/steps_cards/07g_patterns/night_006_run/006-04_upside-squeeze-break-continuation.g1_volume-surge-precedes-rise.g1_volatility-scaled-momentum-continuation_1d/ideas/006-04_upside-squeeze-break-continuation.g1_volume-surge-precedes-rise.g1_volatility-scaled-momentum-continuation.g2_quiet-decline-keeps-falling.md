---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 10-day return is negative, the narrower its 10-day average daily range relative to its 60-day average range, the more its price falls below its usual 3-day return over the next 3 days.
Consequence: A quiet, sagging coin is a reason to refuse a long and to lean short for the next few days, rather than to wait for a breakout.
Why:
- F5: Range compression did not precede larger moves, which goes against the brief. The size of the next 3-day move, as a multiple of the coin's mean, was 0.97 after the most compressed ranges (10-day mean range over 60-day, bottom quintile). The middle quintiles gave 0.91 to 0.92, and the most expanded ranges gave 1.22. Expanded ranges were also followed by a higher excess return, +0.0065 (t 1.92), against −0.0055 (t −2.01) after compressed ones.
- F6: Range compression combined with a falling 10-day return was followed by a further fall. Compressed ranges with a negative 10-day return gave −0.0092 excess (t −3.16, n 664). Expanded ranges with a positive 10-day return gave +0.0097 (t 2.69, n 684).
- F4: Light volume is costly when the advance is weak. Bars in the lowest volume tercile give −0.0089 excess (t −2.65, n 485) when the scaled 10-day return is also in its lowest tercile, and −0.0093 (t −2.98, n 566) when it is in its middle tercile. Within the top scaled-return tercile, the middle volume tercile is where the gain sits, at +0.0106 (t 3.08, n 463).
