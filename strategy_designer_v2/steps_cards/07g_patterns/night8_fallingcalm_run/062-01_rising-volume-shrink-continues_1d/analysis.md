---
line: 7.g patterns
backtest: 062-01_rising-volume-shrink-continues_1d
idea tested: 062-01_rising-volume-shrink-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3694 USD
---
## Findings
- **F1:** In rising markets (60-day return above +10 %), the raw 30-day against prior-30-day log volume ratio predicts the 5-day excess return in the idea's direction, with slope −0.0365 and t −2.65 over 318 non-overlapping cases; the most-shrunk quintile (log ratio −1.22 to −0.36) gains +4.84 % (t 2.17, 64 cases) and the most-grown quintile loses −1.07 % (t −0.57). The tested pipeline (standardised over 60 values, clipped at 0) only reached t 0.87.
- **F2:** Inside rising markets the effect lives in the agitated half (20-day swing above the coin's median), where shrunk-volume cases gain +2.43 % (39 cases), middle +0.60 % (45) and grown-volume −3.04 % (62), a graded spread of about 5.5 %; in the calm half there is no order (shrunk +3.21 %, middle +1.18 %, grown +3.85 %).
- **F3:** Outside rising markets the sign reverses: the volume-ratio slope is +0.0198 (t 2.13, 528 cases) and the most-shrunk quintile loses −2.33 % (t −2.05), so shrinking volume comes before falls there, which is source brief 060's own idea, not a new one.
- **F4:** Across all profiles, a coin's 5-day return scaled by its 20-day swing predicts its next 5 days (slope 0.0104, t 3.33, 1422 cases; top quintile +1.72 %, t 2.34; in rising markets top quintile +3.49 %, t 2.68), a short-term continuation the rising-continuation strategies already on the map (034-01.e1, 034-02, 033-03.b2) most likely hold.
- **F5:** Daily returns are highest on Thursdays (+0.61 %, t 4.10, 1242 days) and Fridays (+0.52 %, t 3.87) and lowest on Wednesdays (−0.35 %, t −1.94); this is a calendar condition that cannot be graded and is close to the held 045-01 "late week gain", so it gives no idea.
- **F6:** The book's gain is thin in every window of folds B and C (mean daily book return from −0.069 % in w16 to +0.277 % in w11). It lags holding in the windows where the coins rose strongly (w11: +0.277 % against +1.256 %; w16: −0.069 % against +0.454 %), which fits a long-only book that is flat on the grown-volume and calm bars of rising markets.

## Ideas
- `062-01.g1_agitated-uptrend-volume-dry-up` (from F1, F2, F6): In a rising, agitated market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
