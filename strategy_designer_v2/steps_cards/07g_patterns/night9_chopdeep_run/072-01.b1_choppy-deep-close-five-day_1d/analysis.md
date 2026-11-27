---
line: 7.g patterns
backtest: 072-01.b1_choppy-deep-close-five-day_1d
idea tested: 072-01.b1_choppy-deep-close-five-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3756 USD
---
## Findings
- **F1:** In choppy bars (regime 'unknown'), the 5-day return minus the coin's normal drift is concentrated in the deepest fifth of closes below the 20-day high, at −6.6 % (t −3.7, 52 non-overlapping cases, depth −9.2 to −4.6 swings). The other four fifths sit between −0.9 % and −0.1 % (all |t| < 0.9). The effect is convex, not linear, which is why the plan's linear slope only reached t 1.08.
- **F2:** By choppy deciles, the two deepest give −6.5 % (t −2.2) and −6.4 % (t −3.1) over 5 days, against −1.5 % to +1.5 % for deciles 2 to 9 (25 cases each). The book's forecast correlates 0.92 with raw depth, and its allocation grows smoothly from −0.22 to −0.80. The book therefore spends most of its short exposure where there is no move.
- **F3:** The deep-close fall in choppy bars holds after down days (−5.3 %, t −2.5, 32 cases) and after up days (−8.4 %, t −2.6, 18 cases). It points the same way in 5 of 6 coins (LTC −0.5 % the exception) and in 2018, 2019 and 2020 (t −2.4, −2.0, −3.2), but not in 2021 (+0.1 %, 9 cases).
- **F4:** The deep-close fall is larger when the coin is swinging more than usual. In the deepest choppy fifth, the 5-day excess is −12.0 % in the high-volatility half (15 cases) against −4.1 % in the low half (35 cases). In choppy bars, the top two volatility terciles give −3.4 % and −3.3 % (70 and 39 cases), against −0.3 % in the lowest (140 cases). The map has no strategy in the choppy agitated short cell.
- **F5:** Per case, the deepest choppy fifth's −6.6 % excess is about 0.6 of the coin's usual 5-day move (10.6 %). That is roughly 35 times the 0.19 % cost of a trade, against the tested idea's average 0.43 % (strength 0.051).
- **F6:** Outside the choppy profile, the sign flips. Closes nearest the 20-day high are followed by +3.5 % over 5 days (t 3.9, 236 cases), and the deepest by −1.2 % (t −1.4). This is nearness-to-high continuation, already held (034-01.b1, 035-01.b1).
- **F7:** Other patterns found are already held:

## Ideas
- `072-01.b1.g1_choppy-convex-deep-close-fall` (from F1, F2, F3, F5): In a choppy market, a coin's fall over the next five days grows faster than its close's depth below its 20-day high, measured in units of the standard deviation of its last 20 days' daily returns. A close twice as deep below the high is followed by much more than twice the fall.
- `072-01.b1.g2_choppy-agitated-deep-close-fall` (from F4, F1, F3): In a choppy, agitated market, the further a coin closes below its 20-day high, in units of the standard deviation of its last 20 days' daily returns, the larger its fall over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
