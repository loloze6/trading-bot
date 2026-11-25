---
line: 7.g patterns
backtest: 041-03_agitated-fall-drop-vs-range-rebound_1d
idea tested: 041-03_agitated-fall-drop-vs-range-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4054 USD
---
## Findings
- **F1:** Inside the falling-agitated profile (16 % of the coins' bars in folds B, C), the next day's excess return grows with the size of the day's fall measured in 30-day mean ranges: +0.60 % (t 1.13, 224 cases) for falls of 0.1–0.4 ranges, +1.83 % (t 2.54, 180) for 0.4–0.8, +2.64 % (t 2.40, 47) for 0.8–1.5 and +6.20 % (t 1.62, 20) beyond 1.5. The fall-weighted mean is +3.07 % (t 2.22, 560 down-days) with a day-clustered slope t of 2.91.
- **F2:** The rebound after falls is specific to the falling-agitated profile. The same fall-weighted next-day excess is −0.56 % (t −0.80, slope t −0.22, 622 down-days) in falling calm markets, +0.15 % (t 0.22) in choppy markets and +0.74 % (t 1.52) in rising markets. Across all out-of-profile bars, the correlation between the scaled move and the next-day excess is −0.03, against −0.21 in the profile.
- **F3:** The brief's mirror half, that up-days give back in this profile, does not stand out. In profile, the up-move-weighted next-day giveback is +0.64 % (t 1.15, 542 up-days) with a slope t of −0.57 (not graded). By bin it changes sign: −1.30 % (t −2.54) after 0.1–0.4-range rises, +1.20 % (t 1.66) after 0.4–0.8 and −2.66 % (t −3.05) after 0.8–1.5. It is negative in 2021 (−1.08 %) and on XRP (−0.96 %).
- **F4:** The rebound after in-profile falls holds on every coin (+0.78 % on BTC, t 1.66, up to +2.23 % on LTC, t 3.01) and in every year shown. Its strength varies widely, from +0.07 % in 2019 (t 0.17) to +3.24 % in 2020 (t 2.91).
- **F5:** The effect is spent after one day. The scaled-move-weighted reversal is +2.00 % on the next day (t 2.33, 1,102 cases) and −0.56 % on the day after (t −0.93). After falls beyond 0.8 ranges, the second day's excess is −1.3 % to −1.6 % (unreliable, under 70 cases).
- **F6:** In profile, closing near the day's low is followed by a next-day excess of +2.17 % (t 2.86, 243 cases), against +0.24 % (t 0.86) out of profile. This is the low-close rebound of the source idea (034-01.d2), already tested, and it overlaps the scaled fall.
- **F7:** The book depends on a few market-wide rebound days. Its top 10 % of days carry 155 % of its net gain. On its best 5 % of days (31 days, book +2.79 %) the coins rose +8.78 % on average, and on its worst 5 % (book −1.16 %) they fell −7.96 %.

## Ideas
- No ideas: Every pattern that stands out (F1, F2, F4, F5, F6) is the tested idea or the already-tested low-close idea from the same profile. The brief's symmetric up-day reversal (F3) is not graded and changes sign. After looking at the scaled move, the close location, profiles, weekdays, coins, years, two- and three-day horizons and the book's extreme days, nothing else stands out enough over the many angles examined to support a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
