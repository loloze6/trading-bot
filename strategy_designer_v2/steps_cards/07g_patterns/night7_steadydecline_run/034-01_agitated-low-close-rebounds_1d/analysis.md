---
line: 7.g patterns
backtest: 034-01_agitated-low-close-rebounds_1d
idea tested: 034-01_agitated-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4347 USD
---
## Findings
- **F1:** In agitated bars the reversal is concentrated in wide-range days. Close location × next-day excess, cases summed per day, gives t 3.03 (mean 0.0068, 451 days) on days with a wide range against the coin's 30-day usual range, against t 0.76 for narrow days (408) and t 0.97 for mid days (507). In a regression of the next-day excess on close location, today's move and close location × (relative range − 1), the interaction has t 6.69 and close location alone t 4.48.
- **F2:** On wide agitated days the signed next-day gain is +1.13 %, +1.42 % and +1.00 % for weak, mid and strong close placement (333, 353 and 314 cases). On narrow days it is +0.17 %, −0.18 % and +0.53 %. That is about three times the idea's average +0.39 % per case and about six times the 0.19 % trade cost.
- **F3:** Within agitated bars the effect lives where the 60-day trend is falling or choppy, not rising. Close location × next-day excess has t 2.57 in falling (mean 0.0105, 229 days), t 2.08 in choppy (84 days) and t −0.64 in rising (270 days). In rising markets the signed gain turns negative for mid and strong placement (−0.20 % and −0.42 %), while in falling markets it is +0.81 % to +1.79 %.
- **F4:** The effect is spent after one day. In agitated bars the t is 2.96 at 1 day (1051 days), 1.26 at 2 days (551) and 0.46 at 3 days (367). In calm bars it is 1.48 at 1 day and −1.09 at 3 days.
- **F5:** Calm bars carry the same width gradient, much weaker. Close location × next-day excess has t 1.70 on wide days against −0.61 on narrow days, against 2.80 and 0.90 in agitated bars.
- **F6:** A large down day (bottom fifth of the day's return scaled by the 30-day swing) is followed in agitated bars by +0.955 % next-day excess (t 3.45, 581 cases) and +2.22 % over 3 days (t 2.74, 178 grid cases). Once close location is in the regression, however, today's scaled move has a positive coefficient (t 2.40), so the one-day rebound is carried by the low close, not by the size of the fall.
- **F7:** Weekday next-day excess looked significant pooled: Wednesday −0.50 % (t −2.78), Thursday +0.41 % (t 2.80) and Friday +0.38 % (t 2.75). The signs flip across years (Wednesday is +0.21 % in 2021, Thursday −0.04 % in 2021), so this is not a finding.
- **F8:** The book's gain is spread evenly. Long and short position gains have the same t (2.95 each; 2783 and 2292 bars), and the book's mean is positive in every year from 2018 to 2021 (0.8 to 2.9 bp a day) whatever the coins did (−33 to +42 bp a day). The book is thin but not carried by one side or one year.

## Ideas
- `034-01.g1_wide-day-close-location-reversal` (from F1, F2, F5, F4): In an agitated market, the wider a coin's day is against its usual daily range over the past 30 days, and the nearer its close sits to the day's low within that range, the larger its rise over the next day; the nearer to the high, the larger its fall.
- `034-01.g2_falling-agitated-low-close-rebound` (from F3, F4, F8): In a falling, agitated market, the nearer a coin's daily close sits to the day's low within its high-low range, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
