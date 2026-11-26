---
line: 7.d confirmed, not profitable
backtest: 060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d
idea tested: 060-02.d1.d2.d1_volume-signal-in-deeper-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5673 USD
---
## Findings
- **F1:** The book's deepest fall, −29.6 % over 24 days in w14 (its days 82 to 105 of 122), came entirely from the long side. All six coins were held long, at mean positions from 0.71 to 1.12, and lost from −0.17 to −0.40 each. In that stretch volume had grown strongly (log ratio 0.53 to 1.30), the 20-day fall was −28 % to −42 % and the 5-day return was −8 % to −12 %. The book was buying volume growth inside a crash that kept going.
- **F2:** The long side's gain sits in the steepest falls only. With the 20-day return below −40 %, longs earned +1.42 % per bar (127 bars, sum +1.81). From −40 % to −15 % they lost (−0.41 % per bar over 181 bars from −40 % to −30 %, −0.15 % over 117 bars from −20 % to −15 %). All other long bins together sum to about −0.23. On the 5-day grid in a falling market, volume up with the 20-day fall below −40 % was followed by +5.7 % over 5 days (20 cases). The condition alone cannot be separated from the signal here: only 1 of the 21 such grid cases had volume down. This depth may therefore carry a rebound effect of its own.
- **F3:** The short (dry-up) side carries the book. It held 1,203 bars at +0.23 % per bar (sum +2.80, against +2.15 for longs, with a lower bar standard deviation, 2.7 % against 4.0 %). Its gain is largest in moderate falls: +0.66 % per bar from −15 % to −10 % and +0.48 % from −20 % to −15 %. On the falling-market grid with the 20-day return between −40 % and −10 %, volume down was followed by −3.0 % over 5 days (111 cases) and volume up by +1.8 % (98). With the 20-day return above −10 %, the two were nearly equal (+0.46 %, 106 cases, against +0.26 %, 65 cases). This is the brief's dry-up continuation, and it lives in real but not extreme falls.
- **F4:** A cost-free proxy of the book shows that each side change cuts the deepest fall and so moves the failing Calmar. The proxy base had a yearly return of 20.1 %, a deepest fall of −29.6 % and a Calmar of 0.68. Short side only gave 11.3 %, −13.4 % and 0.85. Shorts plus longs only below a −40 % 20-day return gave 19.5 %, −14.9 % and 1.31, with Sharpe rising from 0.97 to 1.14. Dropping longs taken after a 5-day rise above 5 % gave 22.0 %, −22.3 % and 0.98.
- **F5:** Longs taken after the coin had already bounced lose. After a 5-day rise above 5 %, longs earned −0.14 % per bar (202 bars). Outside the deepest falls they lost the same, −0.14 % (183 bars), against +0.10 % (611) without the bounce. On the grid with the 20-day return below −10 %, volume up after a bounce was followed by −0.04 % (19 cases), against +2.9 % without one (99). The condition alone is partly an effect of its own: volume down after a bounce gave −4.5 % (11) against −2.7 % (101). A bounce therefore removes the long side's edge but sharpens the short side's.

## Ideas
- `060-02.d1.d2.d1.d1_dry-up-shorts-in-real-falls` (from F3, F4, F1): In a falling market, the more the coin's trading volume over the past 30 days has shrunk against the 30 days before, the further it falls over the next 5 days, and the more so while its 20-day return is a real fall rather than a slight dip.
- `060-02.d1.d2.d1.d2_volume-growth-buys-steepest-crashes` (from F2, F1, F3, F4): In a falling market, the more the coin's trading volume over the past 30 days has grown against the 30 days before, the larger its rise over the next 5 days, and the more so the steeper its 20-day fall, the rise appearing only in the steepest falls. The more volume has shrunk instead, the further the coin falls over the next 5 days in a real fall.
- `060-02.d1.d2.d1.d3_volume-growth-before-the-bounce` (from F5, F4, F1): In a falling market, the more the coin's trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 5 days, the more so the deeper its 20-day fall, and the less so the more the coin has already risen over the past 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
