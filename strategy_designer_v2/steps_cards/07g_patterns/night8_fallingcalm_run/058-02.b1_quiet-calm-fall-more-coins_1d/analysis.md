---
line: 7.g patterns
backtest: 058-02.b1_quiet-calm-fall-more-coins_1d
idea tested: 058-02.b1_quiet-calm-fall-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4150 USD
---
## Findings
- **F1:** Across all profiles, the sharper a coin's one-day fall, the more it gains the next day. In the decile of the most negative daily return scaled by 20-day swing, the next-day excess return is +0.85 % (t 3.87, 767 non-overlapping days); in the next decile it is +0.48 % (t 2.53); it then falls steadily to −0.48 % in decile 7 (t −2.78). This next-day rebound after a sharp fall is already held many times on the profile map (falling agitated, agitated, and the 77 long books acting in every profile), so it is not a discovery.
- **F2:** In the falling calm profile, the rebound in F1 is absent. After the sharpest-fall quintile the next day is −0.09 % (t −0.34, 347 days). Every quintile's next-day excess is negative, from −0.09 % to −0.57 %, the largest in the middle quintile (t −2.83), so continuation there is not graded by the day's move.
- **F3:** The tested idea's own grading does not show in folds B and C. Inside falling calm, the 5-day excess by 30-day-return quartile is −0.60 %, −2.73 %, +0.25 %, +0.06 % (76–77 cases each). By 5-day/30-day volume quartile it is −1.41 %, −0.49 %, −0.04 %, −1.06 %. Neither is monotone, matching step 5's failed supporting check (larger-minus-smaller half −0.003 %).
- **F4:** The strongest falling-calm 5-day cell is the second daily-return quartile at −3.83 % (t −3.91, 90 cases), and it is a grid artifact. The same quintile on the five possible 5-day grid offsets gives −1.31 % at offset 0 but +0.82 %, +0.10 %, +1.17 % and +0.24 % at offsets 1 to 4. It also holds only in 2018–2019 (−2.96 %, −4.22 %) and not in 2020–2021 (+0.83 %, −0.26 %).
- **F5:** Weekday effects reach |t| 2.1–2.9 on next-day returns (Wednesday −0.51 %, t −2.90; Tuesday +0.36 %, t 2.14) but change sign across years. Wednesday is −1.40 % in 2019 but +0.03 % in 2020, and Tuesday −1.37 % in 2018 but +1.44 % in 2021. Given the roughly 30 groupings looked at, none stands out from chance.
- **F6:** The book is a hedge against the coins rather than a timing edge. Its daily returns correlate −0.39 with the coins' returns. Its best 1 % of days (+5.36 %) came when the coins fell 9.79 %, and its worst 1 % (−4.52 %) when they rose 6.70 %. Its gain is concentrated in w14 (+0.22 % a day while the coins fell 0.56 %).

## Ideas
- No ideas: The only pattern that clearly beats chance across the many angles examined (the next-day rebound after a sharp one-day fall, F1) is already held many times on the profile map. The falling-calm continuation (F2) is not graded by any situation measured (F2, F3), and the other candidates are grid or year artifacts or multiple-testing noise (F4, F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
