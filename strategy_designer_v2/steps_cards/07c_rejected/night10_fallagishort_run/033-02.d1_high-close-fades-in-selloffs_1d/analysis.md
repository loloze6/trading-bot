---
line: 7.c no effect
backtest: 033-02.d1_high-close-fades-in-selloffs_1d
idea tested: 033-02.d1_high-close-fades-in-selloffs
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3737 USD
---
## Findings
- **F1:** Inside the falling agitated profile the market rebounds after closes near the low, which is the long side, not the short. On 384 in-profile days, the lowest fifth of close locations was followed by a next-day excess return of +2.30 % (t 2.95, 76 cases). The highest fifth was followed by only −0.65 % (t −0.97, 77 cases), and the middle fifths by +0.42 %, +0.30 % and −0.02 %. A short-only book therefore pays the bounce on most of its bars, and the forecast-weighted short excess is +0.14 % (t 0.27, 382 cases on 230 days).
- **F2:** The ordering by close location does point the idea's way, but it is weak. The correlation of close location with the next-day excess return is negative on every coin: XMR −0.26 (t −2.68, 99), LTC −0.12 (t −1.72, 209) and BCH −0.14 (t −1.21, 75). By year it is 2020 −0.34 (t −4.25, 141), 2019 −0.17, 2021 −0.10 and 2018 +0.01. Outside the profile, the highest fifth of closes is followed by −0.55 % (t −2.63, 695 cases).
- **F3:** In the profile, what the next day does follows the day's own direction more than its close location. After the largest fifth of down days (open to close) the next day is +3.36 % (t 3.56, 76 cases), and after the second fifth +1.46 % (t 2.03). Down days that also closed in the low half give a short −1.85 % (t −2.80, 168 cases on 114 days). Those down days, together with the low-close bounce in F1, are what the tested short loses on.
- **F4:** Taking up days only, a short graded by close location earns +0.88 % next day (t 1.47, 188 cases, 115 days). LTC gives +1.12 % (t 2.00, 97), XMR +0.68 % (t 0.98) and BCH +0.54 % (t 0.49). Up days that close in the high half give +0.76 % (t 1.30, 158 cases).
- **F5:** The tested idea's one-day horizon is too short; the late chase reverses over about three days. On days that closed up, a short graded by the size of the day's rise earns +4.11 % excess over the next 3 days (t 2.42, 61 non-overlapping cases on 39 days). Graded by the 1-day close-to-close rise it earns +4.27 % (t 2.50, 63 cases). The same short graded by close location instead earns only +1.12 % (t 0.94).
- **F6:** The 3-day result in F5 holds on every coin and every year, though it is weaker in 2021.
- **F7:** The tested idea's size cannot carry the cost of a trade. Its unusual move is +0.11 % per case and its total move +0.05 %, against a 0.35 % cost per trade. A 3-day move of about +4 % on up days (F5) is more than ten times that cost.

## Ideas
- `033-02.d1.c1_chased-rallies-fade-three-days` (from F5, F6, F3, F7): In a falling, agitated market, when a coin's day rises and closes near its high, the larger that day's rise, the larger the fall in its price over the next three days.
- `033-02.d1.c2_high-close-on-up-days` (from F4, F2, F1, F3): In a falling, agitated market, on days a coin closes above its open, the nearer its daily close sits to that day's high, measured as its position within the day's high-low range, the larger the fall in its price over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
