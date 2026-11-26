---
line: 7.g patterns
backtest: 047-02_falling-agitated-daily-rise-giveback_1d
idea tested: 047-02_falling-agitated-daily-rise-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4155 USD
---
## Findings
- **F1:** In the recorded falling, agitated profile, down days show a graded next-day rebound. The coin's next-day excess return falls by 1.06 % per unit of standardised one-day return (t −3.77, 557 cases on 236 days), and the mean next-day excess is +1.26 %, about 6.6 times the 0.19 % cost of a trade.
- **F2:** On up days in the same profile, the next-day fall that the tested idea predicts is not graded. The slope is +0.22 % per unit with t 0.66 (540 cases), against a level mean next-day excess of −0.98 %, so the giveback does not grow with the size of the rise.
- **F3:** Within the profile, the size of the day's move is what carries the reversal, not where the bar closed. In a joint regression the standardised return has t −2.06 (−0.69 % per unit) and the close location t −0.43 (1,097 cases, 388 days).
- **F4:** Across all bars, the lower a coin closes within its day's range, the higher its next-day excess return: −1.19 % per unit of centred close location (t −3.04, 8,330 cases on 1,448 days).
- **F5:** The close-location effect grows with how wide the day is against the coin's usual range. In a regression on close location and close location × relative range, the interaction carries the effect (all bars t −2.32, in the profile t −3.59 % per unit with t −2.76), while close location alone becomes insignificant (t 1.01).
- **F6:** The close-location effect sits in falling and choppy markets and is absent in rising ones.
- **F7:** The one-day close-location reversal is partly undone on the second day: the day-two slope is +0.87 % (t 2.32) on all bars and +2.45 % (t 2.59) in the profile.
- **F8:** Next-day excess by weekday is not stable from year to year. For example, Sunday is −127 bp in 2018 and +122 bp in 2020, and Wednesday is −160 bp in 2019 and +21 bp in 2021, so it gives no idea.

## Ideas
- `047-02.g1_falling-agitated-fall-rebound` (from F1, F2, F3): In a falling, agitated market, the larger a coin's one-day percent fall, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `047-02.g2_wide-day-close-location-reversal` (from F4, F5, F6, F7): The lower a coin closes within its day's high-low range, and the wider that range is against the coin's usual daily range, the larger its rise over the next day. The higher it closes in a wide day's range, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
