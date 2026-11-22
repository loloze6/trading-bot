---
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3893 USD
---
## Findings
- **F1:** On the non-overlapping 18-bar (3-day) grid, the top fifth of the volume ratio (4h volume over its 180-bar mean) is followed by an excess 3-day return of +1.03 % (z +0.113, t 3.14, n 1059). The other four fifths are all negative (z −0.060 to −0.018, n about 1058 each). The rise after a surge is concentrated in the extreme fifth, not graded across the range, which matches the near-zero Spearman of the volume ratio with the excess (0.048, n 5580).
- **F2:** The surge pays when it comes on top of a 3-day rise. Coins in the top third of the past 3-day return with the top third of the volume ratio gained +0.95 % excess over the next 3 days (z +0.108, t 2.50, n 730). The same top third of past return with low or middle volume ratio gave nothing (z −0.003, t −0.08, n 465; z −0.008, t −0.18, n 569).
- **F3:** The brief's exhaustion pattern does not appear. After a 3-day rise in the top third, a fading volume trend (last day's volume against the last 3 days, bottom third) is followed by z −0.001 (t −0.02, n 548), not a give-back. A rising volume trend is followed by continuation: z +0.105, t 2.42, n 664, +0.95 %.
- **F4:** Quiet, directionless stretches are followed by falls. Coins in the middle third of the past 3-day return with the low third of the volume ratio lost −0.78 % excess over the next 3 days (z −0.077, t −2.94, n 761), and with the middle third −0.56 % (t −2.26, n 595). The 2nd and 3rd fifths of the past 3-day return show z −0.053 (t −1.98) and −0.076 (t −2.98), n 1116 each.
- **F5:** By count of rising bars in the past 18, the excess rises with persistence: 10–12 rising bars give z +0.054 (t 1.73, n 1108) and 13–18 give z +0.122 (t 1.61, n 234). The 7–8 bucket gives z −0.112 (t −3.58, n 989), so the effect is not monotone.
- **F6:** Grid cells starting on a Sunday are followed by an excess 3-day return of −1.23 % (z −0.150, t −4.05, n 811). The other weekdays lie between z −0.036 and +0.080. This is the strongest single cell among roughly 90 examined, but it is a calendar effect with no graded situation, and the book's daily returns by weekday do not show it (Monday +0.014 %, Tuesday +0.042 %).
- **F7:** The book's largest days are the coin's: its best 1 % of days average +17.8 % against the coin's +17.2 %, and its worst 1 % average −15.2 % against −14.5 % (n 174 each). Its tail days carry no timing beyond exposure, which fits the failed Calmar (0.56).

## Ideas
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.g1_volume-confirmed-rally-continues` (from F1, F2, F3, F5): When a coin has risen over the past three days and its latest four-hour volume is high against its 30-day average, it keeps rising over the next three days. The larger the 3-day rise and the higher that volume against its average, the larger the further rise.
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.g2_quiet-sideways-drift-lower` (from F4, F1): When a coin's price has barely moved over the past three days and its four-hour volume is below its 30-day average, it falls relative to its usual drift over the next three days. The further its volume sits below that average, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
