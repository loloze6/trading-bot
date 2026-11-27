---
line: 7.g patterns
backtest: 077-01_choppy-calm-swing-rise-carries_1d
idea tested: 077-01_choppy-calm-swing-rise-carries
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4045 USD
---
## Findings
- **F1:** Inside the choppy calm profile, the 14-day return divided by the 30-day daily swing ranks the coin's next 7-day unusual move in the same direction (Spearman rho 0.25, p 0.006, 122 non-overlapping cases), while outside the profile it does not (rho 0.06, p 0.12, all trends together).
- **F2:** The downward half carries too, and this side was never tested. In the choppy calm profile, a swing-scaled 14-day fall below -0.5 is followed by a further 7-day fall: the unusual move in the short direction is +3.2 %, t 2.33 with cases of one day taken together, 22 cases. That compares with +4.6 %, t 1.86, 35 cases for rises above +0.5.
- **F3:** The short side is positive in every year shown: 2018 +1.2 % (7 cases), 2019 +3.7 % (5), 2020 +3.3 % (3), 2021 +4.9 % (7). It is positive on 4 of 5 coins, all but BTC (BTC -3.2 %, 4 cases). Each cell is small.
- **F4:** The carry is not an artefact of one sampling grid. The in-profile rho between the swing-scaled move and the 7-day unusual move is positive at all 7 grid offsets (0.08 to 0.31; p < 0.02 at 4 of them). The mean after falls is negative at 6 of 7 offsets and the mean after rises is positive at all 7.
- **F5:** The carry lives in the calm half of the choppy market only. On choppy bars outside the profile, which are the agitated ones, the same rank correlation is -0.01 (p 0.81, 248 cases).
- **F6:** The carry is concentrated in the largest moves. In the profile, a swing-scaled rise above 1.5 is followed by +10.3 % unusual over 7 days (t 2.31, 13 cases), while 1.0 to 1.5 gives -1.0 % (7 cases). In the book, trades entered at forecast 18.9 to 20 averaged +3.67 % net (80 trades), against -0.95 % (40 trades) for lower entries.
- **F7:** The 7-day horizon reads clearest. The rank correlation is 0.07 (p 0.25) at 3 days, 0.25 (p 0.006) at 7 days and 0.19 (p 0.17) at 14 days.
- **F8:** Other angles mostly repeat held ideas: next-day rebounds after a daily fall of more than 2 swings outside the profile (+2.1 %, t 3.5, 131 days) and late-week gains (Thursday +0.57 %, t 3.9; Friday +0.53 %, t 3.9). Both are already held strategies.

## Ideas
- `077-01.g1_choppy-calm-swing-fall-carries` (from F2, F3, F4, F5): In a choppy, calm market, a coin whose 14-day return is large and negative against its own daily swing over the past 30 days keeps falling over the next 7 days, and the larger that swing-scaled fall, the larger the further fall.
- `077-01.g2_choppy-calm-two-sided-swing-carry` (from F1, F2, F4, F5, F6, F7): In a choppy, calm market, a coin's 14-day return measured against its own daily swing over the past 30 days is followed by a 7-day move the same way, up after a rise and down after a fall, and the further more the larger the swing-scaled move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
