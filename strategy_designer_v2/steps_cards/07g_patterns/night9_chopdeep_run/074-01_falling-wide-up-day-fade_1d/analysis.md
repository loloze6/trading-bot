---
line: 7.g patterns
backtest: 074-01_falling-wide-up-day-fade_1d
idea tested: 074-01_falling-wide-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3803 USD
---
## Findings
- **F1:** In a falling market the wide-up-day fade lives in agitated stretches only (30-day swing above the coin's median). After an up day wider than its 20-day mean range, the next day's return minus drift is -1.38 % in agitated stretches (t -2.26 with one day's cases taken together; 223 cases on 111 days). In calm stretches it is -0.28 % (t -0.71; 154 cases on 97 days).
- **F2:** Inside falling agitated stretches the fade grows with width. By range-multiple tercile of the wide up days, the next day's return minus drift is -0.85 % (t -1.07, 58 days), then -1.32 % (t -1.48, 46 days), then -1.94 % (t -2.18, 49 days). In calm stretches the narrowest tercile is followed by a rise, +0.62 % (t 1.00).
- **F3:** Across the whole falling market, the fade after wide up days points the same way in most windows. The next-day return minus drift is negative in 7 of the 10 windows with cases (w14 -2.62 %, t -2.05; w16 -1.52 %, t -1.52). It is positive in w12, w17 and w18, all with t under 0.9.
- **F4:** The mirror in falling agitated stretches is stronger. A down day wider than its 20-day mean range is followed by +1.85 % next day (t 2.90; 270 cases on 115 days), against +0.31 % (t 0.78) after narrow down days. This rebound is already held: 16 long strategies in falling agitated, among them 044-01 "agitated wide range fall rebound". It is not a discovery.
- **F5:** The other angles show nothing that survives taking one day's cases together:
- **F6:** The book stayed small, which is why it paid little:

## Ideas
- `074-01.g1_falling-agitated-wide-up-fade` (from F1, F2, F3): In a falling, agitated market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day. The wider that range is against the 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
