---
line: 7.g patterns
backtest: 077-01.b1.b1_choppy-agitated-low-close-rebound_1d
idea tested: 077-01.b1.b1_choppy-agitated-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4311 USD
---
## Findings
- **F1:** Only days much wider than usual carry the rebound after a low close. On days closing in the bottom quarter of their range, the next-day excess return is +0.02 % (t 0.07, 962 cases) at up to 1.0x the 20-day mean range and −0.03 % (t −0.06, 249) at 1.0–1.25x. It rises to +1.27 % (t 2.82, 190 cases, 128 days) at 1.25–1.5x, +1.10 % (t 2.30, 176) at 1.5–2x and +2.60 % (t 1.88, 102) above 2x. The tested config's width cut of 1.0 therefore spent most of its cases where there is no effect.
- **F2:** The rebound after very wide low-close days lasts beyond the next day. For days of at least 1.5x the mean range closing in the bottom quarter (278 cases, 130 days), the excess return is +1.67 % over 2 days (t 2.62) and +2.40 % over 3 days (t 2.86). The sign is positive in every year shown (2018 +0.5 %, 2019 +1.2 %, 2020 +3.5 %, 2021 +1.2 %) and on every coin with enough cases (BTC +1.1 %, ETH +1.7 %, XRP +4.0 %, XMR +1.4 %).
- **F3:** Inside the book's choppy agitated profile (4.6 % of bars), very wide days closing in the bottom fifth rose +2.33 % the next day (t 2.06, only 14 cases on 11 days). Narrower in-profile low closes rose +0.42 % (t 0.58, 45 cases). The profile adds little evidence of its own; the step-5 size of +0.37 % (t 1.12) is diluted by narrow days.
- **F4:** In a falling market (60-day return below −10 %), days of at least 1.25x the mean range closing in the top quarter fall the next day by −1.89 % excess (t −2.59, 116 cases, 54 days). The sign is negative in every year (2018 −1.8 %, 2019 −2.2 %, 2020 −3.8 %, 2021 −0.3 %). The same days in a rising market rise +0.68 % (t 1.10, 225 cases), and in a choppy market they fall −0.91 % (t −1.20, 59 cases).
- **F5:** Wide low-close days (≥1.5x range, bottom quarter) rebound most in a rising market: +2.40 % next day (t 3.41, 65 cases, 39 days). In a falling market the rebound is +1.90 % (t 0.93, 72 cases) and in a choppy market +1.40 % (t 1.27, 36 cases).
- **F6:** The book earned almost all its gain on a few days. Its 10 best days sum to +9.2 % of a +11.0 % total over 1,449 days, against −2.1 % for its 10 worst days. With 2 % of coin-days in a position, the Calmar of 0.24 comes from a gain too rare to outgrow its falls.
- **F7:** Other angles showed nothing that stands out:

## Ideas
- `077-01.b1.b1.g1_choppy-agitated-very-wide-rebound` (from F1, F2, F3): In a choppy, agitated market, a day that closes near its low rises over the next three days, by more the wider that day's range is against the coin's range over the past 20 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `077-01.b1.b1.g2_falling-market-wide-high-fade` (from F4): In a falling market, a day that closes near its high falls over the next day, by more the wider that day's range is against the coin's range over the past 20 days.
- `077-01.b1.b1.g3_rising-market-wide-dip-rebound` (from F5, F2): In a rising market, a day that closes near its low rises over the next three days, by more the wider that day's range is against the coin's range over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
