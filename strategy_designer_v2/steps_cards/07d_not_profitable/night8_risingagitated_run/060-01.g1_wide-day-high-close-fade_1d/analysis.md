---
line: 7.d confirmed, not profitable
backtest: 060-01.g1_wide-day-high-close-fade_1d
idea tested: 060-01.g1_wide-day-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4473 USD
---
## Findings
- **F1:** The book fails on trading too little (0.0051 trades per day against 0.01; 1 % of coin-days in a position) and on Calmar (0.38). The Calmar fails because the yearly return is only +2.0 %, not because of large falls: the deepest window fall is -1.44 % (w18) and the worst book day is -1.31 %. On folds B and C the book held a short on 36 coin-days, earning +2.21 % per held day at a mean allocation of -0.56.
- **F2:** The tested situation is narrow (close location ≥ 0.75 and range ≥ 1.5 times the 20-day mean, in profile), giving only 36 cases on 20 days, +2.37 % short-direction unusual move, t 1.64. The broader case of the same situation (close in the upper part of the range, at least 0.6, on a day at least as wide as its 20-day mean) gives 118 cases on 70 days, +1.91 %, t 2.47. That is more than three times the trades, with the same strength and a surer t. Close ≥ 0.5 with range ≥ 1.0 gives 133 cases, +1.56 %, t 2.02.
- **F3:** The effect is graded by the range multiple inside the broader case (close ≥ 0.6, in profile): +1.73 % (41 cases) at 1.0–1.2×, +0.49 % (29) at 1.2–1.5×, +2.51 % (31) at 1.5–2×, and +3.67 % (17) above 2×.
- **F4:** The effect is graded by where the close sits, on in-profile days at least as wide as usual. A close in the lower half is followed by the coin rising (short-direction -2.85 % in 0–0.25, 100 cases; -2.66 % in 0.25–0.5, 77 cases). The fade appears from the middle up: +0.99 % in 0.5–0.75 (52 cases) and +2.42 % in 0.75–0.9 (57 cases). The very top (>0.9) gives +0.76 % on 24 cases.
- **F5:** Neither condition earns alone, so both belong to the idea:
- **F6:** The effect lives in the agitated downtrend, as the theory says.
- **F7:** The fade is a one-day move. At two days the broader in-profile case on a 2-day grid gives +0.92 %, t 0.84, over 72 cases, against +1.91 % at one day. A longer holding would dilute it.
- **F8:** The fade is not carried by one coin: every coin's mean is positive in the broader case, from +1.20 % (BTC, 29 cases) to +3.94 % (XRP, 14 cases). It is mostly carried by w14 (35 cases, +2.73 %), w16 (34, +1.98 %) and w18 (17, +2.39 %). w13 (9, -0.48 %) is the only clearly negative window.

## Ideas
- `060-01.g1.d1_wider-than-usual-high-close-fade` (from F1, F2, F3, F5, F7): In a falling, agitated market, a coin that closes in the upper half of a day whose high-low range is at least as wide as its average range of the last 20 days falls over the next day. The wider that day's range against its recent ranges, the larger the fall.
- `060-01.g1.d2_wide-day-close-location-graded-fade` (from F1, F2, F4, F5, F6): In a falling, agitated market, a coin whose day's high-low range is at least as wide as its average range of the last 20 days falls over the next day when it closes above the middle of that range. The higher the close sits above the middle of the range, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
