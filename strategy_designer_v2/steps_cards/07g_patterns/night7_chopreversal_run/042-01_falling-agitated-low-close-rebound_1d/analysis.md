---
line: 7.g patterns
backtest: 042-01_falling-agitated-low-close-rebound_1d
idea tested: 042-01_falling-agitated-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4199 USD
---
## Findings
- **F1:** Inside the falling agitated profile the effect sits almost entirely in the bottom fifth of the day's range: closes there are followed by a next-day excess return of +2.17 % (t 4.97, 243 cases), the fourth fifth by +0.35 % (t 1.28), and the top three fifths by -0.49 %, -0.84 % (t -2.46) and -0.06 %, so the rise is not linear in the close's place.
- **F2:** Day size multiplies the effect inside the profile. On days wider than the coin's last 20 days, the close-location slope is 0.070 (t 3.64, 332 cases, 163 days), against 0.014 (t 0.99) on narrow days. Bottom-fifth closes on wide days gain +3.97 % the next day (t 2.60, 72 cases, 39 days), against +1.41 % (t 1.78) on ordinary days.
- **F3:** The close's distance below the day's high, measured in the coin's usual daily range (its last 20 days' mean range), predicts more sharply than the close's share of the day's range. In profile its slope t is 5.84 (1194 cases, 430 days), against 2.95 for the share, and it stays at 2.63 without w16. Its top fifth gains +2.86 % the next day (t 3.68), and the other four fifths are all between -0.16 % and -0.48 %.
- **F4:** Outside the profile, the same deep close on a wide day also rebounds: bottom-fifth closes on wide days gain +1.05 % the next day (t 2.49, 321 cases, 161 days), against -0.17 % on ordinary days. The distance below the high in usual ranges has a slope t of 2.30 out of profile (6447 cases), with its top fifth at +0.59 % (t 2.10).
- **F5:** The rebound is a one-day move. In profile, the next-three-day slope has a t of 0.59, against 2.95 over one day, and bottom-fifth closes are only +0.93 % up after two days (t 1.11) against +2.17 % after one.
- **F6:** In profile, the day's own open-to-close return predicts the next day against itself, with a slope of -0.22 (t -3.53, 1298 cases, 467 days), against -0.0009 out of profile.
- **F7:** The book's gain is concentrated. 2020 carries 0.355 of the summed 0.481 of daily returns, and window w16 alone 0.318. The 10 best days add up to 113 % of the total, and 7 of the 10 worst days fall in w14. In-profile bottom closes gain +5.93 % in 2020 (t 3.31), but only +0.32 % in 2021 (t 0.32). The Calmar failure comes from a gain that arrives in a few bursts.

## Ideas
- `042-01.g1_deep-close-in-usual-ranges` (from F1, F2, F3, F5): In a falling, agitated market, the farther a coin's close sits below that day's high, measured in the coin's usual daily range over the last 20 days, the larger its rise over the next day, the largest after a wide day that closes at its low.
- `042-01.g2_wide-low-close-rebounds` (from F3, F4, F5): The farther a coin's close sits below that day's high, measured in the coin's usual daily range over the last 20 days, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `042-01.g3_agitated-down-day-next-day-rebound` (from F6, F5): In a falling, agitated market, the larger a coin's fall from that day's open to its close, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
