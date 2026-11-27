---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4985 USD
---
## Findings
- **F1:** The book's gain is cut by its exit, not by the signal: trades that ended with the coin's 60-day trend already falling earned +12.78 % each (29 trades, sum +370.8 %), while those that ended still choppy lost −2.10 % (14) and those that ended rising lost −7.08 % (5). Trades closed within 3 days lost −3.56 % each (41 trades, sum −145.8 %), and trades held 3 to 5.5 days earned +2.04 % (66), 5.5 to 8 days +1.97 % (21) and over 8 days +4.99 % (9). Covering when the profile ends gives up the part of the fall that pays.
- **F2:** The effect is larger over a longer horizon. On the non-overlapping grid inside the profile, high-close bars after a negative 5-day return had an unusual short move of +9.02 % over 2 days (t 3.54, 22 cases), +12.08 % over 5 days (t 3.35, 22) and +14.42 % over 10 days (t 3.20, 13). Outside the profile the same bars earn nothing over 5 days (−0.26 %, t −0.37, 317 cases), so the effect lives in choppy agitated markets only.
- **F3:** The failing Sharpe against holding (0.31 vs 0.55) and the Calmar of 0.43 come from a book that is rarely in the market and lightly sized. It holds a position on 5 % of the coins' days, its mean absolute allocation is 0.35, its daily standard deviation is 0.51 %, and its yearly return is +2.6 %. Its deepest falls (−5.5 % in w15 and in w16) sit in windows where w16 alone carried +23.6 % of the summed gain.
- **F4:** Signals on an up day lose and those on a down day pay. Trades entered on a day that closed up about +8.6 % lost −3.31 % each (46 trades, sum −152.4 %), while those entered on a day that closed down about −3.1 % earned +3.19 % (46, sum +146.9 %). The fading close works when the day was a fall recovered off its low, not a rebound day. Down closes without the high close do not earn: in the profile, low-close bars after a negative 5-day return had an unusual short move of −1.36 % over 5 days (22 cases).
- **F5:** The deeper the 5-day fall, the stronger the effect, and only together with the high close. In the profile, high-close bars after a 5-day fall deeper than one usual 5-day swing had an unusual short move of +31.0 % over 5 days (6 cases), and shallower negative falls +9.7 % (9). Negative 5-day falls without a high close had only +0.8 % (14), so the depth alone is not the effect. Among signals, the deep and mid thirds of the 5-day fall gave +20.0 % and +17.0 %, against +0.8 % for the shallow third.
- **F6:** Losses gather where the price rose right after entry. Trades whose price went more than 10 % above the entry lost a combined −293.9 % (24 trades). ZEC carried −150.6 % over 28 trades, including two w11 trades of −62.8 % and −32.1 %, so a few adverse squeezes set the falls.

## Ideas
- `061-01.b1.b1.b1.d1.d2.d1.d2.d1_upper-close-fade-held-ten-days` (from F1, F2, F3): In a choppy, agitated market, when a coin's daily close sits in the upper half of that day's high-low range after its 5-day return has been negative, its price falls over the next ten days, keeping on falling after its 60-day trend turns to falling, the fall growing with the depth of that 5-day fall.
- `061-01.b1.b1.b1.d1.d2.d1.d2.d2_down-day-upper-close-fade` (from F4, F6, F2): In a choppy, agitated market, when a coin's day closed lower than the day before yet sits in the upper half of its high-low range, after its 5-day return has been negative, its price falls over the next five days, the fall growing with the depth of that 5-day fall.
- `061-01.b1.b1.b1.d1.d2.d1.d2.d3_swing-scaled-upper-close-fade` (from F5, F3): In a choppy, agitated market, when a coin's daily close sits in the upper half of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, the fall growing with how many of the coin's usual 5-day swings that 5-day fall spans.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
