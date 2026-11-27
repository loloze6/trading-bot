---
line: 7.d confirmed, not profitable
backtest: 081-01_deep-up-day-next-day-fade_1d
idea tested: 081-01_deep-up-day-next-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4097 USD
---
## Findings
- **F1:** The fade sits almost entirely in the deepest fifth of up days by depth: the next-day excess return is −1.00 % (t −5.49, 1049 cases), against −0.27 % (t −1.70) in the second fifth and +0.26 % (t 1.24) in the shallowest; the book gains 0.69 % per active bar in the deepest fifth against a cost of 0.059 %, but −0.04 % in the middle fifth and −0.04 % in the shallowest (cost 0.018 %), so the shallow shorts the standardised forecast still takes eat the gain and pull the mean daily return on days in a position down to 0.040 %.
- **F2:** For the deepest fifth the fade grows with the horizon: the excess is −1.26 % over 3 days (t −2.45, 360 non-overlapping cases) and −4.04 % over 5 days (t −4.24, 175 cases), four times the one-day move and about 18 times the 0.22 % cost of a trade; the shallowest fifth instead rises +5.87 % over 5 days (t 2.57), so a short there loses.
- **F3:** In a rising 60-day trend the book loses (−0.013 % per bar, against +0.153 % in falling and +0.138 % in choppy markets); the deepest up days fall −0.83 % next day in falling and −0.80 % in choppy markets but only −0.17 % in rising ones, where all bars drift +0.60 % a day. Being out of rising markets is not an effect on its own: falling and choppy bars alone move +0.04 % and −0.04 % the next day, nothing a short earns.
- **F4:** The falls come in strong rallies: in w11 the coins rose +1.93 % a day and the book lost −0.13 % a day, and on the 10 % strongest coin days the book loses −0.96 % against +1.68 % on the 10 % weakest days, which is the short book's exposure behind the 0.17 Calmar.
- **F5:** Depth alone after a down day gives no next-day fade (deepest fifth +0.86 %, shallowest +0.89 %), as the theory says. Over 3 days the deepest down days lag the drift by −0.65 %, half the up days' −1.46 % (−0.72 % against the 0.75 % drift), so the up-day condition still carries most of the effect at the longer horizon.
- **F6:** Turnover is high for the move captured: a held position averages 0.45 of the book and changes by 0.33 of the book per held bar, so about three-quarters of each position is traded every day for a one-day move whose total is 0.9 times the cost.

## Ideas
- `081-01.d1_deep-up-day-five-day-fade` (from F2, F6, F5): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next five days.
- `081-01.d2_deepest-up-days-carry-fade` (from F1, F2): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, the fall growing faster than the depth so that the up days furthest below the high, in swing units, carry most of it.
- `081-01.d3_deep-up-day-fade-outside-uptrends` (from F3, F4): In any market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, except when the coin has been rising over the last 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
