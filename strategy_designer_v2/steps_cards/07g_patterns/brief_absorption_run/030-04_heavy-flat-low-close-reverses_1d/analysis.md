---
line: 7.g patterns
backtest: 030-04_heavy-flat-low-close-reverses_1d
idea tested: 030-04_heavy-flat-low-close-reverses
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4003 USD
---
## Findings
- **F1:** On heavy-volume days (volume at least 2× the prior 20-day mean, first per 5-day grid cell), a close in the upper third of the range was followed by a 5-day excess move of +0.149 usual moves (t 2.56, n 341), or +1.76 % excess and +2.38 % total (t 3.47), well above the 0.19 % cost of a trade. Heavy days closing mid-range gave −0.007 (t −0.10, n 246), and heavy days closing in the lower third gave +0.045 (t 0.72, n 253).
- **F2:** The upper-close effect belongs to heavy volume: on ordinary-volume days (volume below 1.5× its mean), an upper-third close gave only +0.026 usual moves (t 0.86, n 951).
- **F3:** The effect is carried by heavy days that also closed up from the open. Heavy days that closed up from the open and in the upper third gave +0.159 (t 2.67, n 300). Heavy days with a positive 1-day return gave +0.123 (t 2.40, n 434), against +0.018 (t 0.33, n 406) when it was negative.
- **F4:** The upper-close effect after heavy days is positive on all 6 coins (from +0.048 on LTC to +0.224 on ZEC, ZEC t 2.03) but unstable across years: +0.587 (t 4.12) in 2024 and +0.491 (t 2.43) in 2020, against −0.304 (t −1.80) in 2018 and −0.185 (t −1.52) in 2022.
- **F5:** The tested book lost because it shorted exactly these days. Its 427 short trades lost −4.45 % each after fees (t −6.66, 23 % winners), on every coin except XMR (+0.07 %) and in every year from 2019. Its 308 long trades earned +2.31 % (t 3.25), and the book's daily mean is within ±0.03 % of zero on every coin.
- **F6:** Grading is weak. The excess move does not rise steadily with heavier volume among upper-close heavy days: +0.152 at 2–2.5×, +0.082 at 2.5–3.5×, +0.271 above 3.5×. The slopes of the excess move over heavy days are t 0.90 on close location × volume ratio, t 0.94 on close location and t 1.63 on the day's return in usual moves (n 840).
- **F7:** Other angles showed nothing that stands out from chance given how many were looked at. These were past 5-day and 20-day return, past 1-day return, volatility level and range size quintiles; the 20-day and 1-day quintiles were non-monotone, with isolated t near ±3. The next-day return by weekday (Friday +0.30 %, t 3.76; Wednesday −0.30 %, t −2.70) gives no graded situation.

## Ideas
- `030-04_heavy-flat-low-close-reverses.g1_heavy-volume-high-close-continues` (from F1, F2, F4, F5): On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 5 days.
- `030-04_heavy-flat-low-close-reverses.g2_heavy-volume-up-day-follows` (from F3, F5, F6): On a day when a coin's volume is far above its 20-day average, the larger that day's rise from its open, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
