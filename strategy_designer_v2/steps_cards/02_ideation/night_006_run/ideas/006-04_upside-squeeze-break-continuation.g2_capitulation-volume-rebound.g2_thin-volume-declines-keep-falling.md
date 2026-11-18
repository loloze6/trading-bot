---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen over the last 5 days, the lower its 5-day average volume against its 30-day average, the larger its further decline over the next 3 days.
Consequence: A trader would refuse to buy, or would short, declines that happen on thin volume, rather than treat every dip as a rebound chance.
Why:
- F3: The effect is graded at both ends, and the thin-volume end is the sharper one. The lowest volume-ratio fifth (mean ratio 0.53) is followed by an excess 3-day return of -0.81% (t -3.05) and the highest fifth (ratio 1.74) by +0.87% (t 2.56). After a 5-day fall the lowest fifth gives -1.39% (t -3.63) and the highest +1.05% (t 2.00).
- F5: The book fails mainly because it is long only after falls. Those cases earn a mean 3-day return of 0.12%, against 0.63% after rises (Welch t -2.08). This leaves the book a mean daily return of 0.0074% and a Sharpe of 0.10, against 0.118% and 0.55 for holding. Its positions do grow with the volume ratio, from 0.24 to 0.82 of the book across fifths.
