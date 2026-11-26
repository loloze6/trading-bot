---
line: 7.g patterns
backtest: 060-02.d3_volume-growth-ten-day-hold_1d
idea tested: 060-02.d3_volume-growth-ten-day-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4542 USD
---
## Findings
- **F1:** In the falling profile with the 20-day return below 0, the 30/30-day log volume ratio ranks the coin's excess return better the longer the horizon. The Spearman rho is 0.165 over 5 days (426 cells, p 0.0006), 0.296 over 10 days (207 cells, p < 0.0001) and 0.300 over 20 days (107 cells, p 0.0017).
- **F2:** Over 20 days the effect holds in both halves of the falling profile. The rho is 0.415 in falling calm (47 cells, p 0.0038) and 0.391 in falling agitated (70 cells, p 0.0008), against 0.18 over 10 days in each (p 0.11 and 0.03).
- **F3:** The falling-profile volume effect at 10 days points the same way in 6 of the 10 windows with at least 8 cells. It reaches rho 0.37 to 0.59 in w7, w13, w15 and w18, but turns to −0.40 in w16 and w17. The tested 10-day measure sits just under the bar: t 1.87 on 147 day-cases.
- **F4:** Outside the falling profile the volume ratio's sign flips. In a rising market (60-day return above +10 %) the rho is −0.168 over 5 days (318 cells, p 0.0026) and −0.154 over 10 days (158 cells, p 0.054). The lowest volume-ratio quartile is followed by a +7.1 % excess 10-day return (t 1.71), the highest by +0.4 %.
- **F5:** In non-falling agitated cells the flip is graded. The rho is −0.232 over 10 days (84 cells, p 0.033), and the highest volume-ratio quartile is followed by a −7.4 % excess 10-day return (33 cells, t −2.19).
- **F6:** In calm markets outside the falling profile, the coin's 20-day return predicts the same sign over the next 10 days with the strongest rank link seen in any angle: rho 0.301 (137 cells, p < 0.0001), and 0.171 over 5 days (277 cells, p 0.0005). In falling calm cells it is 0.162 (p 0.087) and 0.159 over 5 days (p 0.016). In agitated cells it is absent (−0.005 to −0.04). It may partly repeat the calm nearness-to-high book 035-01.b1 already held.
- **F7:** The book earns about the same on long and short days, so the volume signal pays on both sides inside the falling profile. Long days average +0.157 % a day (1,399 coin-days) and short days +0.143 % (1,837 coin-days). The losing windows are w10–w12 and w18, at −0.009 % to −0.072 % a day.
- **F8:** The angles that showed nothing distinguishable from chance were the close position in the day's range, the day's range, the 1-day return and the weekday. Every one of their Spearman p-values was above 0.16, except the 10-day volume ratio at p 0.028, which is weak after about 60 tests.

## Ideas
- `060-02.d3.g1_volume-growth-twenty-day-hold` (from F1, F2, F3, F7): In a falling market, while the coin's 20-day return is still negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 20 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.d3.g2_rising-volume-surge-fades` (from F4, F5): In a rising market, the more the coin's trading volume over the past 30 days has grown against the 30 days before, the smaller its rise, or the larger its fall, over the next 5 days.
- `060-02.d3.g3_calm-market-twenty-day-momentum` (from F6): In a calm market, the higher the coin's 20-day return, the larger its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
