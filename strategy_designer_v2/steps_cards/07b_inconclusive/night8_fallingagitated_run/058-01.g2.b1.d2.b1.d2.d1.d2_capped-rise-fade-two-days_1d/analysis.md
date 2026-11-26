---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4047 USD
---
## Findings
- **F1:** The tested two-day measure is on the predicted side but tiny, so no rule could decide it. Capped up days (0 < rise ≤ one 30-day swing) in the falling-agitated profile gave back 0.33 % (rise 0–0.5 swing, t 0.58, 191 cases) and 0.48 % (0.5–1 swing, t 0.36, 83 cases) of unusual move over 2 days. This matches step 5's +0.15 % (t 0.39, 501 days).
- **F2:** The give-back of a capped rise shows over the next day. On the same in-profile capped up days, the next-day unusual move in the short direction is +1.04 % (day-clustered t 2.26, 207 days, 517 cases). The total move is +0.84 %, about 3.8 times the 0.22 % cost of a trade. It is lost again by day 2 (F1).
- **F3:** The one-day give-back is broad, not carried by one part of the data. It is positive in every year (2018 2.2 %, 2019 0.9 %, 2020 0.1 %, 2021 1.2 %) and on all 10 coins (0.1 % to 2.4 %). Only w11 (−4.8 %, 12 cases) and w8 (3 cases) are negative among the windows.
- **F4:** The give-back belongs to the profile. Outside it, up days of 0–1 swing show a 2-day unusual move of only 0.00 % to 0.26 % (769 and 460 cases). Inside it, every up-day bin of 0–1 swing is positive at 1 day (0.97 % with t 3.37, and 1.18 % with t 2.15).
- **F5:** At one day the give-back is barely graded within the cap, and it vanishes above it. The Spearman of the rise with the next-day move is 0.03 on capped cases. By quartile of all in-profile up days: 1.02 % (mean rise 0.08 swing), 0.83 % (0.29), 1.47 % (0.60), and 0.12 % for the top quartile (mean rise 1.43 swings).
- **F6:** The grading the brief predicts shows only over longer horizons, on all in-profile up days without the cap. The Spearman of the rise with the short-direction move is 0.23 at 3 days (p 0.0004, 225 cases), 0.26 at 5 days (p 0.02, 78 cases) and 0.39 at 10 days (p 0.009, 43 cases). The 3-day means rise from −0.7 % (0–0.5 swing) to 1.7 % (0.5–1), 2.2 % (1–1.5), 3.5 % (1.5–2) and 6.3 % (2–3), but the overall mean is only 0.70 % (t 1.03).
- **F7:** The brief's own multi-day situation shows nothing. After a positive 3-day rise scaled by swing, the 1–5-day unusual moves are −0.04 % to 1.5 % with clustered t ≤ 1.01. After a 5-day rise they are −0.6 % to 0.1 % with t ≤ 0.06, and the Spearman stays at 0.11 or below.
- **F8:** More data cannot clear up the two-day result. The test already used all 19 coins on all four folds, so only a change of horizon gives a clearer answer.

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1.d2.b1_capped-rise-fade-next-day` (from F1, F2, F3, F4, F5, F8): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day, only while that rise stays within about one usual swing.
- `058-01.g2.b1.d2.b1.d2.d1.d2.b2_graded-rise-fade-three-days` (from F6, F1, F8): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
